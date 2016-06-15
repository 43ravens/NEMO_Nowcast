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

"""NEMO_Nowcast manager.
"""
import argparse
import logging
import logging.config
import os
import pprint
import signal

import yaml
import zmq

from nemo_nowcast import lib


def main():
    """
    Setup and run the nowcast system manager.

    See :command:`python -m nowcast.manager -help`
    for details of the command-line interface.
    """
    mgr = NowcastManager()
    mgr.setup()
    mgr.run()


class NowcastManager:
    """Construct a :py:class:`nemo_nowcast.manager.NowcastManager` instance.
    """
    def __init__(self, name='manager'):
        #: The name of the manager instance.
        #: Used in the nowcast messaging system and for logging.
        self.name = name
        #: :py:class:`dict` containing the nowcast system configuration
        #: that was read from the configuration file.
        self.config = None
        #: Logger for the manager.
        #: Configured by the :kbd:`logging` section of the configuration file.
        self.logger = logging.getLogger(self.name)
        #: Logger for the nowcast system checklist that the manager maintains.
        #: Used to store the checklist on disk whenever it is updated.
        #: Doing so facilitates user inspection of the checklist and thence
        #: the present state of the nowcast system.
        #: It also allows the manager to be restarted with its state preserved.
        #: Configured by the :kbd:`logging` section of the configuration file.
        self.checklist_logger = logging.getLogger('checklist')
        #: Nowcast system checklist: :py:class:`dict` containing the present
        #: state of the nowcast system.
        self.checklist = {}
        #: :py:class:`argparse.Namespace` instance containing the arguments
        #: and option flags and values parsed from the command-line when the
        #: manager was started.
        self._parsed_args = None
        #: :py:class:`zmq.Context` instance that provides the basis for the
        #: nowcast messaging system.
        self._context = zmq.Context()
        #: :py:class:`zmq.Context.socket` instance that is connected to the
        #: message broker to enable nowcast system messages to be exchanged
        #: with worker processes.
        self._socket = None

    def setup(self):
        """Set up the nowcast system manager process including:

        * Building the command-line parser, and parsing the command-line used
          to launch the manager
        * Reading and parsing the configuration file given on the command-line
        * Configuring the logging system as specified in the configuration file
        * Logging the manager's PID, and the file path/name that was used to
          configure it.

        The set-up is repeated if the manager process receives a HUP signal
        so that the configuration can be re-loaded without having to stop and
        re-start the manager.
        """
        self._parsed_args = self._cli()
        self.config = lib.load_config(self._parsed_args.config_file)
        logging.config.dictConfig(self.config['logging'])
        self.logger.info('running in process {}'.format(os.getpid()))
        self.logger.info('read config from {.config_file}'.format(
            self._parsed_args))

    def _cli(self, args=None):
        """Configure command-line argument parser and return parsed arguments
        object.
        """
        base_parser = lib.basic_arg_parser(
            self.name, description=__doc__, add_help=False)
        parser = argparse.ArgumentParser(
            prog=base_parser.prog,
            description=base_parser.description,
            parents=[base_parser])
        parser.add_argument(
            '--ignore-checklist', action='store_true',
            help='''
            Don't load the serialized checklist left by a previously
            running manager instance.
            ''',
        )
        return parser.parse_args(args)

    def run(self):
        """Run the nowcast system manager:

        * Create the :py:class:`zmq.Context.socket` for communication with the
          worker processes and connect it to the message broker.
        * Install signal handlers for hangup, interrupt, and kill signals.
        * Launch the manager's message processing loop
        """
        self._socket = self._context.socket(zmq.REP)
        zmq_host = self.config['zmq']['server']
        zmq_port = self.config['zmq']['ports']['backend']
        self._socket.connect(
            'tcp://{host}:{port}'.format(host=zmq_host, port=zmq_port))
        self.logger.info(
            'connected to {host} port {port}'
            .format(host=zmq_host, port=zmq_port))
        self._install_signal_handlers(zmq_host, zmq_port)
        if not self._parsed_args.ignore_checklist:
            self._load_checklist()
        self._process_messages()

    def _install_signal_handlers(self, zmq_host, zmq_port):
        """Set up hangup, interrupt, and kill signal handlers.
        """
        def sighup_handler(signal, frame):
            self.logger.info(
                'hangup signal (SIGHUP) received; reloading configuration')
            self._socket.disconnect(
                'tcp://{host}:{port}'.format(host=zmq_host, port=zmq_port))
            self.setup()
            self.run()
        signal.signal(signal.SIGHUP, sighup_handler)

        def sigint_handler(signal, frame):
            self.logger.info(
                'interrupt signal (SIGINT or Ctrl-C) received; shutting down')
            self._socket.close()
            raise SystemExit
        signal.signal(signal.SIGINT, sigint_handler)

        def sigterm_handler(signal, frame):
            self.logger.info(
                'termination signal (SIGTERM) received; shutting down')
            self._socket.close()
            raise SystemExit
        signal.signal(signal.SIGTERM, sigterm_handler)

    def _load_checklist(self):
        """Load the serialized checklist left on disk by a previously
        running manager instance.
        """
        checklist_file = self.config['checklist file']
        try:
            with open(checklist_file, 'rt') as f:
                self.checklist = yaml.safe_load(f)
                self.logger.info(
                    'checklist read from {}'.format(checklist_file))
                self.logger.info(
                    'checklist:\n{}'.format(pprint.pformat(self.checklist)))
        except FileNotFoundError as e:
            self.logger.warning('checklist load failed: {}'.format(e))
            self.logger.warning('running with empty checklist')

    def _process_messages(self):
        """Process messages from workers.
        """
        while True:
            self.logger.debug('listening...')
            try:
                message = self._socket.recv()
                # reply, next_steps = self._message_handler(message)
                # self._socket.send_string(reply)
                # if next_steps is not None:
                #     for next_step, next_step_args in next_steps:
                #         next_step(*next_step_args)
            except zmq.ZMQError as e:
                # Fatal ZeroMQ problem
                self.logger.critical('ZMQError:', exc_info=e)
                self.logger.critical('shutting down')
                break
            except SystemExit:
                # Termination by signal
                break
            except Exception as e:
                self.logger.critical('unhandled exception:', exc_info=e)
                self.logger.critical('shutting down')


if __name__ == '__main__':
    main()  # pragma: no cover
