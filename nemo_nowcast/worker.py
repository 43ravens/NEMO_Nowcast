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
from collections import namedtuple
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


class NextWorker(namedtuple('NextWorker', 'name, args')):
    """Construct a :py:class:`nemo_nowcast.worker.NextWorker` instance.

    Intended for use in a nowcast system implementation's
    :py:mod:`nowcast.next_workers` module where :py:func:`after_worker_name`
    functions return lists of :py:class:`nemo_nowcast.worker.NextWorker`
    instances that provide the sequence of workers and their arguments
    that are to be launched next.

    :arg str name: Name of the worker module including its package path,
                   in dotted notation;
                   e.g. :kbd:`nowcast.workers.download_weather`.

    :arg list args: Arguments to use when the worker is launched.
                    Defaults to an empty list.
    """
    def __new__(cls, name, args=[]):
        return super(NextWorker, cls).__new__(cls, name, args)


class NowcastWorker:
    """Construct a :py:class:`nemo_nowcast.worker.NowcastWorker` instance.
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
        #: Function to be called to do the worker's job.
        #: Called with the worker's parsed command-line arguments
        #: :py:class:`argparse.Namespace` instance,
        #: and the worker's configuration dict.
        self.worker_func = None
        #: Function to be called when the worker finishes successfully.
        #: Called with the worker's parsed command-line arguments
        #: :py:class:`argparse.Namespace` instance.
        #: Must return a string whose value is a success message type defined
        # for the worker in the nowcast configuration file.
        self.success = None
        #: Function to be called when the worker fails. Called with the
        # worker's parsed command-line arguments
        #: :py:class:`argparse.Namespace`; instance.
        #: Must return a string whose value is a failure message type defined
        # for the worker in the nowcast configuration file.
        self.failure = None
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

    def run(self, worker_func, success, failure):
        """Prepare the worker to do its work, then do it.

        Preparations include:

        * Parsing the worker's command-line argument into a
          :py:class:`argparse.ArgumentParser.Namepsace` instance

        * Reading the nowcast configuration file named on the command
          line to a dict

        * Configuring the worker's logging interface

        * Configuring the worker's interface to the nowcast messaging
          framework

        * Installing handlers for signals from the operating system

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
        self._parsed_args = self.arg_parser.parse_args()
        self.config = lib.load_config(self._parsed_args.config_file)
        logging.config.dictConfig(self.config['logging'])
        if self._parsed_args.debug:
            root_logger = logging.getLogger()
            for handler in root_logger.handlers:
                if handler.name == 'console':
                    handler.setLevel(logging.DEBUG)
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
        zmq_port = self.config['zmq']['ports']['workers']
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
        """Execute the worker function, communicate its success or failure to
        the nowcast manager via the messaging framework, and handle any
        exceptions it raises.
        """
        try:
            checklist = self.worker_func(
                self._parsed_args, self.config)
            msg_type = self.success(self._parsed_args)
            self._tell_manager(msg_type, checklist)
        except WorkerError:
            msg_type = self.failure(self._parsed_args)
            self._tell_manager(msg_type)
        except SystemExit:
            # Normal termination
            pass
        except:
            self.logger.critical('unhandled exception:', exc_info=True)
            self._tell_manager('crash')
        self._context.destroy()
        self.logger.debug('task completed; shutting down')

    def _tell_manager(self, msg_type, payload=None):
        """Exchange messages with the nowcast manager process.

        Message is composed of worker's name, msg_type, and payload.
        Acknowledgement message from manager process is logged,
        and payload of that message is returned.

        :arg str msg_type: Key of the message type to send;
                           must be defined for worker name in the configuration
                           data structure.

        :arg payload: Data object to send in the message;
                      e.g. dict containing worker's checklist of
                      accomplishments.

        :returns: Payload included in acknowledgement message from manager
                  process.
        """
        try:
            worker_msgs = self.config['message registry']['workers'][self.name]
        except (KeyError, TypeError):
            raise WorkerError(
                'worker not found in {config_file} message registry: {name}'
                .format(config_file=self.config['config_file'], name=self.name))
        try:
            msg_words = worker_msgs[msg_type]
        except (KeyError, TypeError):
            raise WorkerError(
                'message type not found for {.name} worker in {config_file} '
                'message registry: {msg_type}'
                .format(
                    self, config_file=self.config['config_file'],
                    msg_type=msg_type))
        if self._parsed_args.debug:
            self.logger.debug(
                '**debug mode** '
                'message that would have been sent to manager: '
                '({msg_type} {msg_words})'
                .format(msg_type=msg_type, msg_words=msg_words))
            return
        # Send message to nowcast manager
        message = lib.serialize_message(self.name, msg_type, payload)
        self._socket.send_string(message)
        self.logger.debug(
            'sent message: ({msg_type}) {msg_words}'
            .format(msg_type=msg_type, msg_words=worker_msgs[msg_type]))
        # Wait for and process response
        msg = self._socket.recv_string()
        message = lib.deserialize_message(msg)
        mgr_msgs = self.config['message registry']['manager']
        try:
            msg_words = mgr_msgs[message.type]
        except KeyError:
            raise WorkerError(
                'message type not found for manager in {config_file} '
                'message registry: {msg_type}'
                .format(
                    self, config_file=self.config['config_file'],
                    msg_type=message.type))
        self.logger.debug(
            'received message from {msg.source}: ({msg.type}) {msg_words}'
            .format(msg=message, msg_words=msg_words))
        return message
