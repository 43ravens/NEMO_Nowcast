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

from nemo_nowcast import (
    CommandLineInterface,
    Config,
    NextWorker,
)


NAME = 'scheduler'
logger = logging.getLogger(NAME)


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

    After the set-up is complete, start the scheduler worker launching loop.

    See :command:`python -m nowcast.scheduler -help`
    for details of the command-line interface.
    """
    cli = CommandLineInterface(
        NAME, package='nemo_nowcast', description=__doc__)
    cli.build_parser()
    parsed_args = cli.parser.parse_args()
    config = Config()
    config.load(parsed_args.config_file)
    logging.config.dictConfig(config['logging'])
    logger.info('running in process {}'.format(os.getpid()))
    logger.info('read config from {.file}'.format(config))
    _install_signal_handlers()
    run(config)


def run(config):
    """Run the nowcast system worker launch scheduler.

    * Prepare the schedule as specified in the configuration file.
    * Loop forever, periodically checking to see if it is time to launch the
      scheduled workers.
    """
    sleep_seconds = _prep_schedule(config)
    while True:
        schedule.run_pending()
        time.sleep(sleep_seconds)


def _prep_schedule(config):
    """Create the schedule to launch workers and set how often it is checked.
    """
    try:
        sleep_seconds = config['scheduled workers'].pop('schedule sleep')
    except (AttributeError, KeyError):
        # Default to checking schedule every 60 seconds if config not provided
        sleep_seconds = 60
    try:
        for worker, params in config['scheduled workers'].items():
            _create_scheduled_job(worker, params, config)
    except (AttributeError, KeyError):
        # Do nothing if scheduled workers config section is missing or empty
        pass
    return sleep_seconds


def _create_scheduled_job(worker_module, params, config):
    try:
        args = params['cmd line opts'].split()
    except KeyError:
        args = []
    worker = NextWorker(worker_module, args)
    job = schedule.every().__getattribute__(params['every']).at(params['at']).do(
        worker.launch, config, NAME)
    return job


def _install_signal_handlers():
    """Set up hangup, interrupt, and kill signal handlers.
    """
    def sighup_handler(signal, frame):
        logger.info(
            'hangup signal (SIGHUP) received; reloading configuration')
        main()
    signal.signal(signal.SIGHUP, sighup_handler)

    def sigint_handler(signal, frame):
        logger.info(
            'interrupt signal (SIGINT or Ctrl-C) received; shutting down')
        raise SystemExit
    signal.signal(signal.SIGINT, sigint_handler)

    def sigterm_handler(signal, frame):
        logger.info(
            'termination signal (SIGTERM) received; shutting down')
        raise SystemExit
    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    main()  # pragma: no cover
