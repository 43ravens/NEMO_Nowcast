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

"""NEMO_Nowcast worker launch scheduler.
"""
import logging
import logging.config
import os
import signal
import time

import schedule
import zmq
import zmq.log.handlers

from nemo_nowcast import CommandLineInterface, Config, NextWorker


NAME = "scheduler"
logger = logging.getLogger(NAME)

context = zmq.Context()


def main():
    """Set up and run the nowcast system worker launch scheduler.

    Set-up includes:

    * Building the command-line parser, and parsing the command-line used
      to launch the scheduler
    * Reading and parsing the configuration file given on the command-line
    * Configuring the logging system as specified in the configuration file
    * Logging the scheduler's PID, and the file path/name that was used to
      configure it.
    * Install signal handlers for hangup, interrupt, and kill signals.

    The set-up is repeated if the scheduler process receives a HUP signal
    so that the configuration can be re-loaded without having to stop and
    re-start the scheduler.

    After the set-up is complete, start the scheduled worker launching loop.

    See :command:`python -m nowcast.scheduler --help`
    for details of the command-line interface.
    """
    cli = CommandLineInterface(NAME, package="nemo_nowcast", description=__doc__)
    cli.build_parser()
    parsed_args = cli.parser.parse_args()
    config = Config()
    config.load(parsed_args.config_file)
    msg = _configure_logging(config)
    logger.info("running in process {}".format(os.getpid()))
    logger.info("read config from {.file}".format(config))
    logger.info(msg)
    _install_signal_handlers()
    run(config)


def _configure_logging(config):
    """Configure the scheduler's logging system interface.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    if "publisher" in config["logging"]:
        # Publish log messages to distributed logging aggregator
        logging_config = config["logging"]["publisher"]
        logging_config["handlers"]["zmq_pub"]["context"] = context
        host = config["zmq"]["host"]
        port = config["zmq"]["ports"]["logging"][NAME]
        addr = "tcp://*:{port}".format(port=port)
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
        msg = "publishing logging messages to {addr}".format(addr=addr)
    else:
        # Write log messages to local file system
        #
        # Replace logging RotatingFileHandlers with WatchedFileHandlers so
        # that we notice when log files are rotated and switch to writing
        # to the new ones
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
    """Run the nowcast system worker launch scheduler.

    * Prepare the schedule as specified in the configuration file.
    * Loop forever, periodically checking to see if it is time to launch the
      scheduled workers.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    sleep_seconds = _prep_schedule(config)
    while True:
        schedule.run_pending()
        time.sleep(sleep_seconds)


def _prep_schedule(config):
    """Create the schedule to launch workers and set how often it is checked.

    :param config: Nowcast system configuration.
    :type config: :py:class:`nemo_nowcast.config.Config`
    """
    sleep_seconds = 60
    try:
        for sched_item in config["scheduled workers"]:
            worker_module = list(sched_item.keys())[0]
            _create_scheduled_job(worker_module, sched_item[worker_module], config)
    except (AttributeError, KeyError):
        # Do nothing if scheduled workers config section is missing or empty
        pass
    return sleep_seconds


def _create_scheduled_job(worker_module, params, config):
    try:
        args = params["cmd line opts"].split()
    except KeyError:
        args = []
    worker = NextWorker(worker_module, args)
    job = (
        schedule.every()
        .__getattribute__(params["every"])
        .at(params["at"])
        .do(worker.launch, config, NAME)
    )
    return job


def _install_signal_handlers():
    """Set up hangup, interrupt, and kill signal handlers.
    """

    def sighup_handler(signal, frame):
        logger.info("hangup signal (SIGHUP) received; reloading configuration")
        main()

    signal.signal(signal.SIGHUP, sighup_handler)

    def sigint_handler(signal, frame):
        logger.info("interrupt signal (SIGINT or Ctrl-C) received; shutting down")
        raise SystemExit

    signal.signal(signal.SIGINT, sigint_handler)

    def sigterm_handler(signal, frame):
        logger.info("termination signal (SIGTERM) received; shutting down")
        raise SystemExit

    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == "__main__":
    main()  # pragma: no cover
