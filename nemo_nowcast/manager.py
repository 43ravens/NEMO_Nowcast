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
import importlib
import logging
import logging.config
import os
import pprint
import signal
import subprocess

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
        #: The :kbd:`message registry` section of
        #: :py:attr:`~nemo_nowcast.manager.config`.
        self._msg_registry = None
        #: Python module that contains functions to calculate lists of workers
        #: to launch after previous workers end their work.
        self._next_workers_module = None
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
        self._msg_registry = self.config['message registry']
        logging.config.dictConfig(self.config['logging'])
        self.logger.info('running in process {}'.format(os.getpid()))
        self.logger.info('read config from {.config_file}'.format(
            self._parsed_args))
        try:
            self._next_workers_module = importlib.import_module(
                self._msg_registry['next workers module'])
        except ImportError:
            self.logger.critical(
                'could not find next workers module: {[next workers module]}'
                .format(self._msg_registry), exc_info=True)
            raise
        self.logger.info(
            'next workers module loaded from {[next workers module]}'
            .format(self._msg_registry))

    def _cli(self, args=None):
        """Configure command-line argument parser and return parsed arguments
        object.
        """
        base_parser = lib.base_arg_parser(
            self.name, package='nemo_nowcast',
            description=__doc__, add_help=False)
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
        zmq_port = self.config['zmq']['ports']['manager']
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
                self._try_messages()
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

    def _try_messages(self):
        """Try to process messages.

        Extracted from the :kbd:`try:` block in :py:meth:`_process_messages`
        so that it can be tested outside of the :kbd:`while True:` loop.
        """
        message = self._socket.recv_string()
        reply, next_workers = self._message_handler(message)
        self._socket.send_string(reply)
        for worker in next_workers:
            self._launch_worker(worker)

    def _message_handler(self, message):
        """Handle message from worker.
        """
        msg = lib.deserialize_message(message)
        if msg.source not in self._msg_registry['workers']:
            reply = self._handle_unregistered_worker_msg(msg)
            return reply, []
        if msg.type not in self._msg_registry['workers'][msg.source]:
            reply = self._handle_unregistered_msg_type(msg)
            return reply, []
        self._log_received_msg(msg)
        if msg.type == 'clear checklist':
            reply = self._clear_checklist()
            return reply, []
        reply, next_workers = self._handle_continue_msg(msg)
        return reply, next_workers

    def _handle_unregistered_worker_msg(self, msg):
        """Emit error message to log about a message received from a worker
        that is not included in the message registry.
        """
        self.logger.error(
            'message received from unregistered worker: {.source}'.format(msg),
            extra={'worker_msg': msg})
        reply = lib.serialize_message(self.name, 'unregistered worker')
        return reply

    def _handle_unregistered_msg_type(self, msg):
        """Emit error message to log about a message type received from a worker
        that is not included in the message registry.
        """
        self.logger.error(
            'unregistered message type received from '
            '{0.source} worker: {0.type}'.format(msg),
            extra={'worker_msg': msg})
        reply = lib.serialize_message(self.name, 'unregistered message type')
        return reply

    def _log_received_msg(self, msg):
        """Emit debug message about message received from worker.
        """
        self.logger.debug(
            'received message from {0.source}: ({0.type}) {msg_words}'
            .format(
                msg,
                msg_words=self._msg_registry['workers'][msg.source][msg.type]),
            extra={'worker_msg': msg})

    def _handle_continue_msg(self, msg):
        """Handle success, failure, or crash message from worker by generating
        list of subsequent workers to launch.
        """
        if msg.payload is not None:
            self._update_checklist(msg)
        importlib.reload(self._next_workers_module)
        try:
            after_func = getattr(
                self._next_workers_module,
                'after_{worker}'.format(worker=msg.source))
        except AttributeError:
            self.logger.critical(
                'could not find after_{worker} in {next_workers} module'
                .format(
                    worker=msg.source,
                    next_workers=self._msg_registry['next workers module']),
                exc_info=True)
            reply = lib.serialize_message(self.name, 'no after_worker function')
            return reply, []
        next_workers = after_func(msg)
        reply = lib.serialize_message(self.name, 'ack')
        return reply, next_workers

    def _update_checklist(self, msg):
        """Update the checklist value at worker's key with the items passed from
        the worker.

        If key is not present in the checklist, add it with the worker
        items as its value.

        Write the checklist to disk as a YAML file so that it can be
        inspected and/or recovered if the manager instance is restarted.
        """
        try:
            key = self._msg_registry['workers'][msg.source]['checklist key']
        except KeyError:
            raise KeyError(
                'checklist key not found for {.source} worker'.format(msg))
        try:
            self.checklist[key].update(msg.payload)
        except (KeyError, AttributeError):
            self.checklist[key] = msg.payload
        self.logger.info(
            'checklist updated with [{0}] items from {1.source} worker'
            .format(key, msg),
            extra={'worker_msg': msg})
        self._write_checklist_to_disk()

    def _write_checklist_to_disk(self):
        """Write the checklist to disk as a YAML file so that it can be
        inspected and/or recovered if the manager instance is restarted.
        """
        with open(self.config['checklist file'], 'wt') as f:
            yaml.dump(self.checklist, f)

    def _launch_worker(self, worker, host='localhost'):
        """Use a subprocess to launch worker on host with args as the
        worker's command-line arguments.

        This method *does not* wait for the subprocess to complete.
        """
        if host == 'localhost':
            cmd = [self.config['python'], '-m']
            config_file = self.config['config_file']
        else:
            cmd = ['ssh', host, self.config['run'][host]['python'], '-m']
            config_file = self.config['run'][host]['config_file']
        cmd.extend([worker.name, config_file])
        if worker.args:
            cmd.extend(worker.args)
        self.logger.info(
            'launching {} on {}'.format(worker, host),
            extra={'worker': worker, 'host': host})
        self.logger.debug('cmd = {}'.format(cmd), extra={'cmd': cmd})
        subprocess.Popen(cmd)

    def _clear_checklist(self):
        """Write the checklist to a log file, then clear it.

        This method is intended to be called in response to a "clear checklist"
        message from the :py:mod:`nemo_nowcast.workers.clear_checklist` worker.
        That worker is typically run once per nowcast cycle (e.g. daily) at the
        end of peocessing, just before rotating the log files via the
        :py:mod:`nemo_nowcast.workers.rotate_logs` worker.
        """
        for handler in logging.getLogger().handlers:
            if handler.name == 'checklist':
                checklist_handler = handler
                break
        else:
            checklist_handler = None
        if checklist_handler is not None:
            self.logger.info('writing checklist to log file')
            self.logger.log(
                checklist_handler.level,
                'checklist:\n{}'.format(pprint.pformat(self.checklist)))
        self.checklist.clear()
        self._write_checklist_to_disk()
        self.logger.info('checklist cleared')
        reply = lib.serialize_message(self.name, 'checklist cleared')
        return reply


if __name__ == '__main__':
    main()  # pragma: no cover
