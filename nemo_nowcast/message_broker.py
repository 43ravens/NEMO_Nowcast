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

"""NEMO_Nowcast ZeroMQ message broker.

This broker provides the static point in the nowcast messaging framework,
allowing the nowcast manager to be restarted more or less at will.
"""
import logging
import logging.config
import os
import signal
import time

import zmq
import zmq.log.handlers

from nemo_nowcast import CommandLineInterface, Config


NAME = "message_broker"
logger = logging.getLogger(NAME)

context = zmq.Context()


def main():
    """Set up and run the nowcast system message broker.

    Set-up includes:

    * Building the command-line parser, and parsing the command-line used
      to launch the message broker
    * Reading and parsing the configuration file given on the command-line
    * Configuring the logging system as specified in the configuration file
    * Log the message broker's PID, and the file path/name that was used to
      configure it.

    The set-up is repeated if the message broker process receives a HUP signal
    so that the configuration can be re-loaded without having to stop and
    re-start the message broker.

    After the set-up is complete, launch the broker message queuing process.

    See :command:`python -m nemo_nowcast.message_broker --help`
    for details of the command-line interface.
    """
    cli = CommandLineInterface(NAME, package="nemo_nowcast", description=__doc__)
    cli.build_parser()
    parsed_args = cli.parser.parse_args()
    config = Config()
    config.load(parsed_args.config_file)
    msg = _configure_logging(config)
    logger.info(f"running in process {os.getpid()}")
    logger.info(f"read config from {config.file}")
    logger.info(msg)
    run(config)


def _configure_logging(config):
    """Configure the message broker's logging system interface.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    if "publisher" in config["logging"]:
        # Publish log messages to distributed logging aggregator
        logging_config = config["logging"]["publisher"]
        logging_config["handlers"]["zmq_pub"]["context"] = context
        host = config["zmq"]["host"]
        port = config["zmq"]["ports"]["logging"][NAME]
        addr = f"tcp://*:{port}"
        logging_config["handlers"]["zmq_pub"]["interface_or_socket"] = addr
        logging.config.dictConfig(logging_config)
        for handler in logger.root.handlers:
            if isinstance(handler, zmq.log.handlers.PUBHandler):
                handler.root_topic = NAME
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
        msg = f"publishing logging messages to {addr}"
    else:
        # Write log messages to local file system
        #
        # Replace logging RotatingFileHandlers with WatchedFileHandlers so
        # that we notice when log files are rotated and switch to writing to
        # the new ones
        logging_config = config["logging"]
        logging_handlers = logging_config["handlers"]
        rotating_handler = "logging.handlers.RotatingFileHandler"
        watched_handler = "logging.handlers.WatchedFileHandler"
        for handler in logging_handlers:
            if logging_handlers[handler]["class"] == rotating_handler:
                logging_handlers[handler]["class"] = watched_handler
                del logging_handlers[handler]["backupCount"]
        logging.config.dictConfig(logging_config)
        msg = "writing logging messages to local file system"
    return msg


def run(config):
    """Run the nowcast system message broker:

    * Create and bind the :py:class:`zmq.Context.socket` instances for
      communication with the manager and worker processes.
    * Install signal handlers for hangup, interrupt, and kill signals.
    * Launch the brokers message queuing process.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    workers_socket, manager_socket = _bind_zmq_sockets(config)
    _install_signal_handlers(workers_socket, manager_socket)
    # Broker messages between workers and manager
    try:
        zmq.device(zmq.QUEUE, workers_socket, manager_socket)
    except zmq.ZMQError as e:
        # Fatal ZeroMQ problem
        logger.critical(f"ZMQError: {e}", exc_info=True)
        logger.critical("shutting down")
    except SystemExit:
        # Termination by signal
        pass
    except:
        logger.critical("unhandled exception:", exc_info=True)
        logger.critical("shutting down")


def _bind_zmq_sockets(config):
    """Create 0mq sockets and bind them to ports.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    workers_socket = context.socket(zmq.ROUTER)
    manager_socket = context.socket(zmq.DEALER)
    workers_port = config["zmq"]["ports"]["workers"]
    workers_socket.bind(f"tcp://*:{workers_port}")
    logger.info(f"worker socket bound to port {workers_port}")
    manager_port = config["zmq"]["ports"]["manager"]
    manager_socket.bind(f"tcp://*:{manager_port}")
    logger.info(f"manager socket bound to port {manager_port}")
    return workers_socket, manager_socket


def _install_signal_handlers(workers_socket, manager_socket):
    """Set up hangup, interrupt, and kill signal handlers.
    """

    def sighup_handler(signal, frame):
        logger.info("hangup signal (SIGHUP) received; reloading configuration")
        workers_socket.close()
        manager_socket.close()
        main()

    signal.signal(signal.SIGHUP, sighup_handler)

    def cleanup():
        workers_socket.close()
        manager_socket.close()
        context.destroy()

    def sigint_handler(signal, frame):
        logger.info("interrupt signal (SIGINT or Ctrl-C) received; shutting down")
        cleanup()
        raise SystemExit

    signal.signal(signal.SIGINT, sigint_handler)

    def sigterm_handler(signal, frame):
        logger.info("termination signal (SIGTERM) received; shutting down")
        cleanup()
        raise SystemExit

    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == "__main__":
    main()  # pragma: no cover
