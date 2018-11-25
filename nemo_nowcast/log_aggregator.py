# Copyright 2016 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast distributed logging aggregator.

This logging aggregator subscribes to a ZeroMQ port to collect logging messages
published by other processes.
It is useful for nowcast systems in which workers run on hosts other than the
one that the manager and message broker run on.
"""
import logging
import logging.config
import os
import signal

import zmq

from nemo_nowcast import CommandLineInterface, Config


NAME = "log_aggregator"
logger = logging.getLogger(NAME)

context = zmq.Context()


def main():
    """Set up and run the nowcast system logging aggregator.

    Set-up includes:

    * Building the command-line parser, and parsing the command-line used
      to launch the log aggregator
    * Reading and parsing the configuration file given on the command-line
    * Configuring the logging system as specified in the configuration file
    * Logging the log aggregator's PID, and the file path/name that was used to
      configure it.

    The set-up is repeated if the log aggregator process receives a HUP signal
    so that the configuration can be re-loaded without having to stop and
    re-start the scheduler.

    After the set-up is complete, start the log message processing launching
    loop.

    See :command:`python -m nowcast.log_aggregator --help`
    for details of the command-line interface.
    """
    cli = CommandLineInterface(NAME, package="nemo_nowcast", description=__doc__)
    cli.build_parser()
    parsed_args = cli.parser.parse_args()
    config = Config()
    config.load(parsed_args.config_file)
    _configure_logging(config)
    logger.info(
        "running in process {}".format(os.getpid()), extra={"logger_name": NAME}
    )
    logger.info("read config from {.file}".format(config), extra={"logger_name": NAME})
    run(config)


def _configure_logging(config):
    """Configure the log aggregator's file system logging system interface.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    # Replace logging RotatingFileHandlers with WatchedFileHandlers so that we
    # notice when log files are rotated and switch to writing to the new ones
    logging_handlers = config["logging"]["aggregator"]["handlers"]
    rotating_handler = "logging.handlers.RotatingFileHandler"
    watched_handler = "logging.handlers.WatchedFileHandler"
    for handler in logging_handlers:
        if logging_handlers[handler]["class"] == rotating_handler:
            logging_handlers[handler]["class"] = watched_handler
            del logging_handlers[handler]["backupCount"]
    logging.config.dictConfig(config["logging"]["aggregator"])


def run(config):
    """Run the nowcast system log aggregator:

    * Create the :py:class:`zmq.Context.socket` instance to use to subscribe
      to logging messages published by other processes.
    * Subscribe to all of the hosts/ports that are configured to publish log
      messages,
      and subscribe to all message topic.
    * Install signal handlers for hangup, interrupt, and kill signals.
    * Launch the logging message aggregation process.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    socket = context.socket(zmq.SUB)
    for publisher, addrs in config["zmq"]["ports"]["logging"].items():
        if not isinstance(addrs, list):
            addrs = [addrs]
        for addr in addrs:
            try:
                host, port = addr.split(":")
            except AttributeError:
                host = config["zmq"]["host"]
                port = addr
            socket.connect("tcp://{host}:{port}".format(host=host, port=port))
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
            logger.info(
                "subscribed to {host} port {port} "
                "for all messages from {publisher}".format(
                    host=host, port=port, publisher=publisher
                ),
                extra={"logger_name": NAME},
            )
    _install_signal_handlers(socket)
    _process_messages(socket)


def _process_messages(socket):
    """Process logging messages from publishers.

    :param socket: ZeroMQ socket to which we are subscribed to receive logging
                   messages.
    :type socket: :py:class:`zmq.Context.socket`
    """
    while True:
        try:
            _log_messages(socket)
        except zmq.ZMQError as e:
            # Fatal ZeroMQ problem
            logger.critical(
                "ZMQError:".format(e), exc_info=e, extra={"logger_name": NAME}
            )
            logger.critical("shutting down", extra={"logger_name": NAME})
            break
        except SystemExit:
            # Termination by signal
            break
        except Exception as e:
            logger.critical(
                "unhandled exception:", exc_info=e, extra={"logger_name": NAME}
            )
            logger.critical("shutting down", extra={"logger_name": NAME})
            break


def _log_messages(socket):
    """Receive logging messages from publishers, parse the logging level,
    publisher's name, and message, and emit them to the file system logging
    handlers.

    :param socket: ZeroMQ socket to which we are subscribed to receive logging
                   messages.
    :type socket: :py:class:`zmq.Context.socket`
    """
    topic, message = socket.recv_multipart()
    logger_name, level = topic.decode().split(".")
    logger.log(
        getattr(logging, level),
        message.decode().strip(),
        extra={"logger_name": logger_name},
    )


def _install_signal_handlers(socket):
    """Set up hangup, interrupt, and kill signal handlers.

    :param socket: ZeroMQ socket to which we are subscribed to receive logging
                   messages.
    :type socket: :py:class:`zmq.Context.socket`
    """

    def sighup_handler(signal, frame):
        logger.info(
            "hangup signal (SIGHUP) received; reloading configuration",
            extra={"logger_name": NAME},
        )
        socket.close()
        main()

    signal.signal(signal.SIGHUP, sighup_handler)

    def cleanup():
        socket.close()
        context.destroy()

    def sigint_handler(signal, frame):
        logger.info(
            "interrupt signal (SIGINT or Ctrl-C) received; shutting down",
            extra={"logger_name": NAME},
        )
        cleanup()
        raise SystemExit

    signal.signal(signal.SIGINT, sigint_handler)

    def sigterm_handler(signal, frame):
        logger.info(
            "termination signal (SIGTERM) received; shutting down",
            extra={"logger_name": NAME},
        )
        cleanup()
        raise SystemExit

    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == "__main__":
    main()
