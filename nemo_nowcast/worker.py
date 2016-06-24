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

"""NEMO_Nowcast worker classes.
"""
import argparse
import logging
import logging.config
import os
import signal

import zmq

from nemo_nowcast import lib


class WorkerError(Exception):
    """Raised when a worker encounters an error or exception that it can't
    recover from.
    """


class NowcastWorker:
    """Construct a :py:class:`nemo_nowcast.manager.NowcastWorker` instance.
    """
    def __init__(self, name, description, package='nowcast.workers'):
        #: The name of the worker instance.
        #: Used in the nowcast messaging system and for logging.
        self.name = name
        #: Description of the worker.
        #: Used in the command-line interface.
        #: Typically the worker module docstring;
        #: i.e. :kbd:`description=__doc__`.
        self.description = description
        #: Name of the package that the worker is part of;
        #: used to build the usage message.
        #: Use dotted notation;
        #: e.g. :kbd:`nowcast.workers`.
        self.package = package
        #: :py:class:`dict` containing the nowcast system configuration
        #: that was read from the configuration file.
        self.config = None
        #: Logger for the worker.
        #: Configured by the :kbd:`logging` section of the configuration file.
        self.logger = logging.getLogger(self.name)
        #: :py:class:`argparse.ArgumentParser` instance configured to provide
        #: the default worker command-line interface that requires
        #: a nowcast config file name,
        #: and provides :kbd:`--debug`,
        #: :kbd:`--help`,
        #: and :kbd:`-h` options
        self.arg_parser = lib.base_arg_parser(
            self.name, description=self.description, package=self.package)
        self.arg_parser.add_argument(
            '--debug', action='store_true',
            help='''
            Send logging output to the console instead of the log file.
            Log messages that would normally be sent to the manager are sent
            to the console,
            suppressing interactions with the manager such as launching other
            workers.
            Intended only for use when the worker is run in foreground
            from the command-line.
            ''',
        )
        #: :py:class:`argparse.Namespace` instance containing the arguments
        #: and option flags and values parsed from the command-line when the
        #: worker was started.
        self._parsed_args = None
        #: :py:class:`zmq.Context` instance that provides the basis for the
        #: nowcast messaging system.
        self._context = zmq.Context()
        #: :py:class:`zmq.Context.socket` instance that is connected to the
        #: message broker to enable nowcast system messages to be exchanged
        #: with manager process.
        self._socket = None

    def add_argument(self, *args, **kwargs):
        """Add an argument to the worker's command-line interface.

        This is a thin wrapper around
        :py:meth:`argparse.ArgumentParser.add_argument` that accepts
        that method's arguments.
        """
        self.arg_parser = argparse.ArgumentParser(
            prog=self.arg_parser.prog,
            description=self.arg_parser.description,
            parents=[self.arg_parser],
            add_help=False,
        )
        self.arg_parser.add_argument(*args, **kwargs)

    def run(self):
        """Prepare the worker to do its work, then do it.
        """
        self._parsed_args = self.arg_parser.parse_args()
        self.config = lib.load_config(self._parsed_args.config_file)
        logging.config.dictConfig(self.config['logging'])
        self.logger.info('running in process {}'.format(os.getpid()))
        self.logger.info('read config from {.config_file}'.format(
            self._parsed_args))
        self._init_zmq_interface()
        self._install_signal_handlers()
        self._do_work()

    def _init_zmq_interface(self):
        """Initialize a ZeroMQ request/reply (REQ/REP) interface.

        :returns: ZeroMQ socket for communication with nowcast manager process.
        """
        if self._parsed_args.debug:
            self.logger.debug('**debug mode** no connection to manager')
            return
        self._socket = self._context.socket(zmq.REQ)
        zmq_host = self.config['zmq']['server']
        zmq_port = self.config['zmq']['ports']['frontend']
        self._socket.connect(
            'tcp://{host}:{port}'.format(host=zmq_host, port=zmq_port))
        self.logger.info(
            'connected to {host} port {port}'
            .format(host=zmq_host, port=zmq_port))

    def _install_signal_handlers(self):
        """Set up interrupt and kill signal handlers.
        """
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

    def _do_work(self):
        pass
