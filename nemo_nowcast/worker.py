# Copyright 2016-2019 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast worker classes.
"""
import logging
import logging.config
import os
import signal
import socket
import subprocess
import time

import attr
import requests
import zmq
import zmq.log.handlers

from nemo_nowcast import CommandLineInterface, Config, Message


class WorkerError(Exception):
    """Raised when a worker encounters an error or exception that it can't
    recover from.
    """


@attr.s
class NextWorker:
    """Construct a :py:class:`nemo_nowcast.worker.NextWorker` instance.

    Intended for use in a nowcast system implementation's
    :py:mod:`nowcast.next_workers` module where :py:func:`after_worker_name`
    functions return lists of :py:class:`nemo_nowcast.worker.NextWorker`
    instances that provide the sequence of workers and their arguments
    that are to be launched next.
    """

    #: Name of the worker module including its package path,
    #: in dotted notation;
    #: e.g. :kbd:`nowcast.workers.download_weather`.
    module = attr.ib()
    #: Arguments to use when the worker is launched.
    #: Defaults to an empty list.
    args = attr.ib(default=attr.Factory(list))
    #: Host to launch the worker on.
    #: Defaults to :kbd:`localhost`
    host = attr.ib(default="localhost")

    def launch(self, config, logger_name):
        """Use a subprocess to launch worker on host with args as the
        worker's command-line arguments.

        :arg config: Nowcast system configuration that was read from the
                     configuration file.
        :type config: :py:class:`nemo_nowcast.config.Config`

        :arg str logger_name: Name of the logger to emit messages on.

        This method *does not* wait for the subprocess to complete.
        """
        logger = logging.getLogger(logger_name)
        if self.host == "localhost":
            cmd = [config["python"], "-m"]
            config_file = config.file
        else:
            enabled_host_config = config["run"]["enabled hosts"][self.host]
            cmd = [
                "ssh",
                self.host,
                "source",
                enabled_host_config["envvars"],
                ";",
                enabled_host_config["python"],
                "-m",
            ]
            config_file = enabled_host_config["config file"]
        cmd.extend([self.module, config_file])
        if self.args:
            cmd.extend(self.args)
        logger.info(f"launching {self}", extra={"worker": self})
        logger.debug(f"cmd = {cmd}", extra={"cmd": cmd})
        subprocess.Popen(cmd)


@attr.s
class NowcastWorker:
    """Construct a :py:class:`nemo_nowcast.worker.NowcastWorker` instance.
    """

    #: The name of the worker instance.
    #: Used in the nowcast messaging system and for logging.
    name = attr.ib()
    #: Description of the worker.
    #: Used in the command-line interface.
    #: Typically the worker module docstring;
    #: i.e. :kbd:`description=__doc__`.
    description = attr.ib()
    #: Name of the package that the worker is part of;
    #: used to build the usage message.
    #: Use dotted notation;
    #: e.g. :kbd:`nowcast.workers`.
    package = attr.ib(default="nowcast.workers")
    #: :py:class:`nemo_nowcast.config.Config` object that holds
    #: the nowcast system configuration that is loaded from the configuration
    #: file in the :py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method.
    config = attr.ib(default=attr.Factory(Config))
    #: Logger for the worker.
    #: Configured from the :kbd:`logging` section of the configuration file
    #: in the :py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method.
    logger = attr.ib(default=None)
    #: :py:class:`nemo_nowcast.cli.CommandLineInterface` object configured
    #: in the :py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method
    #: to provide the default worker command-line interface that requires
    #: a nowcast config file name,
    #: and provides :kbd:`--debug`,
    #: :kbd:`--help`,
    #: and :kbd:`-h` options.
    cli = attr.ib(default=None)
    #: Function to be called to do the worker's job.
    #: Called with the worker's parsed command-line arguments
    #: :py:class:`argparse.Namespace` instance,
    #: the worker's configuration dict,
    #: and the :py:meth:`~nemo_nowcast.worker.NowcastWorker.tell_manager`
    #: method.
    #: Passed as an argument to the
    #: :py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method.
    worker_func = attr.ib(default=None)
    #: Function to be called when the worker finishes successfully.
    #: Called with the worker's parsed command-line arguments
    #: :py:class:`argparse.Namespace` instance.
    #: Must return a string whose value is a success message type defined
    #: for the worker in the nowcast configuration file.
    #: Passed as an argument to the
    #: :py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method.
    success = attr.ib(default=None)
    #: Function to be called when the worker fails. Called with the
    #: worker's parsed command-line arguments
    #: :py:class:`argparse.Namespace`; instance.
    #: Must return a string whose value is a failure message type defined
    #: for the worker in the nowcast configuration file.
    #: Passed as an argument to the
    #: :py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method.
    failure = attr.ib(default=None)
    #: :py:class:`argparse.Namespace` instance containing the arguments
    #: and option flags and values parsed from the command-line when the
    #: :py:meth:`~nemo_nowcast.worker.NowcastWorker.setup method is called.
    _parsed_args = attr.ib(default=None)
    #: :py:class:`zmq.Context` instance that provides the basis for the
    #: nowcast messaging system.
    _context = attr.ib(default=attr.Factory(zmq.Context))
    #: :py:class:`zmq.Context.socket` instance that is connected to the
    #: message broker to enable nowcast system messages to be exchanged
    #: with manager process.
    #: Created when the
    #: py:meth:`~nemo_nowcast.worker.NowcastWorker.run` method is called.
    _socket = attr.ib(default=None)

    def init_cli(self):
        """Initialize the worker's command-line interface.

        The default worker command-line interface requires a nowcast config
        file name, and provides :kbd:`--debug`, :kbd:`--help`,
        and :kbd:`-h` options.

        Use the :py:meth:`~nemo_nowcast.cli.CommandLineInterface.add_argument`
        method to add worker-specific arguments and/or options to the interface.
        The :py:meth:`~nemo_nowcast.cli.CommandLineInterface.add_date_option`
        method is also available for the common task of adding a date option
        (e.g. :kbd:`--run-date`) to the interface.
        """
        self.cli = CommandLineInterface(
            self.name, description=self.description, package=self.package
        )
        self.cli.build_parser()
        self.cli.parser.add_argument(
            "--debug",
            action="store_true",
            help="""
            Send logging output to the console instead of the log file,
            and suppress messages to the nowcast manager process.
            Nowcast system messages that would normally be sent to the manager
            are logged to the console,
            suppressing interactions with the manager such as launching other
            workers.
            Intended only for use when the worker is run in foreground
            from the command-line.
            """,
        )

    def run(self, worker_func, success, failure):
        """Prepare the worker to do its work, then do it.

        Preparations include:

        * Parsing the worker's command-line argument into a
          :py:class:`argparse.ArgumentParser.Namepsace` instance

        * Reading the nowcast configuration file named on the command
          line to a dict

        * Configuring the worker's logging interface

        * Installing handlers for signals from the operating system

        * Configuring the worker's interface to the nowcast messaging
          framework

        :arg worker_func: Function to be called to do the worker's job.
                          Called with the worker's parsed command-line
                          arguments
                          :py:class:`argparse.Namespace`
                          instance,
                          and the worker's configuration dict.
        :type worker_func: Python function

        :arg success: Function to be called when the worker finishes
                      successfully.
                      Called with the worker's parsed command-line
                      arguments
                      :py:class:`argparse.Namespace`
                      instance.
                      Must return a string whose value is a success
                      message type defined for the worker in the nowcast
                      configuration file.

        :type success: Python function

        :arg failure: Function to be called when the worker fails.
                      Called with the worker's parsed command-line
                      arguments
                      :py:class:`argparse.Namespace`
                      instance.
                      Must return a string whose value is a failure
                      message type defined for the worker in the nowcast
                      configuration file.

        :type failure: Python function
        """
        self.worker_func = worker_func
        self.success, self.failure = success, failure
        self._parsed_args = self.cli.parser.parse_args()
        self.config.load(self._parsed_args.config_file)
        msg = self._configure_logging()
        self.logger.info(f"running in process {os.getpid()}")
        self.logger.info(f"read config from {self.config.file}")
        if not self._parsed_args.debug:
            self.logger.info(msg)
        self._install_signal_handlers()
        self._init_zmq_interface()
        self._do_work()

    def _configure_logging(self):
        """Configure the worker's logging system interface.
        """
        self.logger = logging.getLogger(self.name)
        if "publisher" in self.config["logging"]:
            # Publish log messages to distributed logging aggregator
            logging_config = self.config["logging"]["publisher"]
            zmq_pub_config = logging_config["handlers"]["zmq_pub"]
            zmq_pub_config["context"] = self._context
            if self.name in self.config["zmq"]["ports"]["logging"]:
                addrs = self.config["zmq"]["ports"]["logging"][self.name]
                addrs = addrs if isinstance(addrs, list) else [addrs]
                ports = set()
                for addr in addrs:
                    try:
                        # host:port
                        port = int(addr.split(":")[1])
                    except AttributeError:
                        # port number
                        port = addr
                    if ports and port not in ports:
                        raise WorkerError(
                            f"workers on difference hosts must use the same port number: "
                            f"{self.name}: {addrs}"
                        )
                    else:
                        ports.add(port)
            else:
                ports = self.config["zmq"]["ports"]["logging"]["workers"]
            for port in ports:
                try:
                    addr = f"tcp://*:{port}"
                    zmq_pub_config["interface_or_socket"] = addr
                    logging.config.dictConfig(logging_config)
                    break
                except (zmq.ZMQError, ValueError):
                    continue
            else:
                raise WorkerError("unable for find port to publish log messages to")
            for handler in self.logger.root.handlers:
                if isinstance(handler, zmq.log.handlers.PUBHandler):
                    handler.root_topic = self.name
                    handler.formatters = {
                        logging.DEBUG: logging.Formatter("%(message)s\n"),
                        logging.INFO: logging.Formatter("%(message)s\n"),
                        logging.WARNING: logging.Formatter("%(message)s\n"),
                        logging.ERROR: logging.Formatter("%(message)s\n"),
                        logging.CRITICAL: logging.Formatter("%(message)s\n"),
                    }
            # Not sure why, but we need a brief pause before we start logging
            # messages
            time.sleep(0.25)
            msg = f"publishing log messages to {addr}"
        else:
            # Write log messages to local file system
            logging_config = self.config["logging"]
            logging.config.dictConfig(logging_config)
            msg = "writing log messages to local file system"
        if self._parsed_args.debug:
            for handler in self.logger.root.handlers:
                if handler.name == "console":
                    # Activate console logging handler at the debug level
                    handler.setLevel(logging.DEBUG)
                else:
                    # Deactivate other logging handlers by setting their
                    # levels very high
                    try:
                        # Assumes that the console logging level in the
                        # config is set to a value >logging.DEBUG
                        console_level = logging_config["handlers"]["console"]["level"]
                    except (KeyError, TypeError):
                        console_level = 100
                    handler.setLevel(console_level)
            msg = "**debug mode** writing log messages to console"
        return msg

    def _install_signal_handlers(self):
        """Set up interrupt and kill signal handlers.
        """

        def sigint_handler(signal, frame):
            self.logger.info(
                "interrupt signal (SIGINT or Ctrl-C) received; shutting down"
            )
            self._socket.close()
            raise SystemExit

        signal.signal(signal.SIGINT, sigint_handler)

        def sigterm_handler(signal, frame):
            self.logger.info("termination signal (SIGTERM) received; shutting down")
            self._socket.close()
            raise SystemExit

        signal.signal(signal.SIGTERM, sigterm_handler)

    def _init_zmq_interface(self):
        """Initialize a ZeroMQ request/reply (REQ/REP) interface.

        :returns: ZeroMQ socket for communication with nowcast manager process.
        """
        if self._parsed_args.debug:
            self.logger.debug("**debug mode** no connection to manager")
            return
        self._socket = self._context.socket(zmq.REQ)
        zmq_host = self.config["zmq"]["host"]
        zmq_port = self.config["zmq"]["ports"]["workers"]
        self._socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
        self._socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 900)
        self._socket.connect(f"tcp://{zmq_host}:{zmq_port}")
        self.logger.info(f"connected to {zmq_host} port {zmq_port}")

    def _do_work(self):
        """Execute the worker function, communicate its success or failure to
        the nowcast manager via the messaging framework, and handle any
        exceptions it raises.
        """
        try:
            checklist = self.worker_func(
                self._parsed_args, self.config, self.tell_manager
            )
            msg_type = self.success(self._parsed_args)
            self.tell_manager(msg_type, checklist)
        except WorkerError:
            msg_type = self.failure(self._parsed_args)
            self.tell_manager(msg_type)
        except SystemExit:
            # Normal termination
            pass
        except:
            self.logger.critical("unhandled exception:", exc_info=True)
            self.tell_manager("crash")
        self.logger.debug("shutting down", extra={"logger_name": self.name})
        self._context.destroy()

    def tell_manager(self, msg_type, payload=None):
        """Exchange messages with the nowcast manager process.

        Message is composed of worker's name, msg_type, and payload.
        Acknowledgement message from manager process is logged and returned.

        :arg str msg_type: Key of the message type to send;
                           must be defined for worker name in the configuration
                           data structure.

        :arg payload: Data object to send in the message;
                      e.g. dict containing worker's checklist of
                      accomplishments.

        :returns: Acknowledgement message from manager process.
        """
        try:
            worker_msgs = self.config["message registry"]["workers"][self.name]
        except (KeyError, TypeError):
            raise WorkerError(
                f"worker not found in {self.config.file} message registry: {self.name}"
            )
        try:
            msg_words = worker_msgs[msg_type]
        except (KeyError, TypeError):
            raise WorkerError(
                f"message type not found for {self.name} worker in {self.config.file} "
                f"message registry: {msg_type}"
            )
        if self._parsed_args.debug:
            self.logger.debug(
                f"**debug mode** message that would have been sent to manager: ({msg_type} {msg_words})"
            )
            return
        # Send message to nowcast manager
        message = Message(self.name, msg_type, payload).serialize()
        self._socket.send_string(message)
        self.logger.debug(
            f"sent message: ({msg_type}) {worker_msgs[msg_type]}",
            extra={"logger_name": self.name},
        )
        # Wait for and process response
        msg = self._socket.recv_string()
        message = Message.deserialize(msg)
        mgr_msgs = self.config["message registry"]["manager"]
        try:
            msg_words = mgr_msgs[message.type]
        except KeyError:
            raise WorkerError(
                f"message type not found for manager in {self.config.file} message registry: {message.type}"
            )
        self.logger.debug(
            f"received message from {message.source}: ({message.type}) {msg_words}",
            extra={"logger_name": self.name},
        )
        return message


def get_web_data(
    file_url,
    logger_name,
    filepath=None,
    session=None,
    chunk_size=100 * 1024,
    wait_exponential_multiplier=2,
    wait_retry_max=256,
    wait_exponential_max=60 * 60,
):
    """Download content from file_url and store it in filepath.

    If the first download attempt fails, retry at exponentially increasing
    intervals until wait_exponential_max is exceeded.
    The first retry occurs after wait_exponential_multiplier seconds
    The delay until the next retry is calculated by multiplying the previous
    delay by wait_exponential_multiplier.

    So, with the default argument values, the first retry will occur
    2 seconds after the download fails, and subsequent retries will
    occur at 4, 8, 16, 32, 64, ..., 256, 256, ..., 3582 seconds after each failure.

    :param str file_url: URL to download content from.

    :param str logger_name: Name of the :py:class:`logging.Logger` to emit
                            messages on.

    :param filepath: File path/name at which to store the downloaded content.
                     If :py:class:`None` (the default) the content is returned.
    :type filepath: :py:class:`pathlib.Path`

    :param session: Session object to use for TCP connection pooling
                    to improve performance for multiple requests to the same
                    host.
                    Defaults to :py:obj:`None` for simplicity,
                    in which case a session is created within the function.
                    If the function is called within loop,
                    the recommended use pattern is to create the session
                    outside the loop as a context manager:

                    .. code-block:: python

                        with requests.Session() as session:
                            for thing in iterable:
                                nemo_nowcast.worker.get_web_data(
                                    file_url, logger_name, filepath, session)

    :type session: :py:class:`requests.Session`

    :param chunk_size: Maximum number of bytes to read into memory at a time
                       and write to disk as the download proceeds.
                       The default value gives performance comparable to
                       :command:`curl` when downloading weather forecast files
                       from the Environment Canada collaboration FTP server.
                       Tuning maybe required for downloads from other sources.

    :param wait_exponential_multiplier: Multiplicative factor that increases
                                        the time interval between retries.
                                        Also the number of seconds to wait
                                        before the first retry.
    :type wait_exponential_multiplier: int or float

    :param wait_retry_max: Maximum number of seconds to wait between retries.
                           This caps the exponential growth of the wait time
                           between retries, but retries continue with this
                           period until wait_exponential_max is reached.
    :type wait_retry_max: int or float

    :param wait_exponential_max: Maximum number of seconds for the final retry
                                 wait interval.
                                 The actual wait time is less than or equal to
                                 the limit so it may be significantly less than
                                 the limit;
                                 e.g. with the default argument values the
                                 final retry wait interval will be 2048
                                 seconds.
    :type wait_exponential_max: int or float

    :return: :py:class:`requests.Response.content`
    :rtype: bytes

    :raises: :py:exc:`nemo_nowcast.workers.WorkerError`
    """
    logger = logging.getLogger(logger_name)
    if session is None:
        session = requests.Session()

    def _get_data():
        try:
            response = session.get(file_url, stream=True)
            response.raise_for_status()
            if filepath is None:
                return response.content
            with filepath.open("wb") as f:
                for block in response.iter_content(chunk_size=chunk_size):
                    if not block:
                        break
                    f.write(block)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            socket.error,
        ) as e:
            logger.debug(f"received {e} from {file_url}")
            raise e

    try:
        return _get_data()
    except:
        wait_seconds = wait_exponential_multiplier
        total_seconds = wait_exponential_multiplier
        retries = 0
        while total_seconds < wait_exponential_max:
            sleep_seconds = min(wait_seconds, wait_retry_max)
            logger.debug(f"waiting {sleep_seconds} seconds until retry {retries + 1}")
            time.sleep(sleep_seconds)
            try:
                return _get_data()
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                socket.error,
            ):
                wait_seconds *= wait_exponential_multiplier
                total_seconds += sleep_seconds
                retries += 1
        logger.error(f"giving up; download from {file_url} failed {retries + 1} times")
        raise WorkerError
