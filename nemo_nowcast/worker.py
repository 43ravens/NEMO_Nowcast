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
import logging

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
            self.name, description=self.description)
        self.arg_parser.add_argument(
            '--debug', action='store_true',
            help='''
            Send logging output to the console instead of the log file.
            Log messages that would normally be sent to the manager to the
            console,
            suppressing interactions with the manager such as launching other
            workers.
            Intended only for use when the worker is run in foreground
            from the command-line.
            ''',
        )
        #: :py:class:`zmq.Context` instance that provides the basis for the
        #: nowcast messaging system.
        self._context = zmq.Context()
        #: :py:class:`zmq.Context.socket` instance that is connected to the
        #: message broker to enable nowcast system messages to be exchanged
        #: with manager process.
        self._socket = None
