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

"""Unit tests for nemo_nowcast.worker module.
"""
import argparse
from collections import namedtuple
import signal
from unittest.mock import (
    call,
    Mock,
    patch,
)

import pytest
import zmq

import nemo_nowcast.lib
from nemo_nowcast.worker import (
    NextWorker,
    NowcastWorker,
    WorkerError,
)


class TestNextWorkerConstructor:
    """Unit tests for NextWorker class constructor.
    """
    def test_default_args(self):
        next_worker = NextWorker('nowcast.workers.download_weather')
        assert next_worker.module == 'nowcast.workers.download_weather'
        assert next_worker.args == []
        assert next_worker.host == 'localhost'

    def test_specified_args(self):
        next_worker = NextWorker(
            'nowcast.workers.download_weather', ['--debug', '00'])
        assert next_worker.module == 'nowcast.workers.download_weather'
        assert next_worker.args == ['--debug', '00']

    def test_specified_host(self):
        next_worker = NextWorker(
            'nowcast.workers.run_NEMO', host='west.cloud')
        assert next_worker.module == 'nowcast.workers.run_NEMO'
        assert next_worker.host == 'west.cloud'


@patch('nemo_nowcast.worker.subprocess')
class TestNextWorkerLaunch:
    """Unit tests for NextWorker.lauch method.
    """
    def test_localhost(self, m_subprocess):
        config = {
            'python': 'nowcast-env/bin/python3',
            'config_file': 'nowcast.yaml',
        }
        next_worker = NextWorker('nowcast.workers.test_worker', ['--debug'])
        next_worker.launch(config, 'test_runner')
        cmd = m_subprocess.Popen.call_args_list[0]
        expected = call(
            ['nowcast-env/bin/python3', '-m', 'nowcast.workers.test_worker',
             'nowcast.yaml', '--debug'])
        assert cmd == expected

    def test_remote_host(self, m_subprocess):
        config = {
            'run': {
                'remotehost': {
                    'python': 'nowcast-env/bin/python3',
                    'config_file': 'nowcast.yaml',
        }}}
        next_worker = NextWorker(
            'nowcast.workers.test_worker', ['--debug'], 'remotehost')
        next_worker.launch(config, 'test_runner')
        cmd = m_subprocess.Popen.call_args_list[0]
        expected = call(
            ['ssh', 'remotehost',
             'nowcast-env/bin/python3', '-m', 'nowcast.workers.test_worker',
             'nowcast.yaml', '--debug'])
        assert cmd == expected

    def test_no_cmdline_args(self, m_subprocess):
        config = {
            'python': 'nowcast-env/bin/python3',
            'config_file': 'nowcast.yaml',
        }
        next_worker = NextWorker('nowcast.workers.test_worker')
        next_worker.launch(config, 'test_runner')
        cmd = m_subprocess.Popen.call_args_list[0]
        expected = call(
            ['nowcast-env/bin/python3', '-m', 'nowcast.workers.test_worker',
             'nowcast.yaml'])
        assert cmd == expected


class TestNowcastWorkerConstructor:
    """Unit tests for NowcastWorker.__init__ method.
    """
    def test_name(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.name == 'worker_name'

    def test_description(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.description == 'description'

    def test_package_default(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.package == 'nowcast.workers'

    def test_package_specified(self):
        worker = NowcastWorker('worker_name', 'description', package='foo.bar')
        assert worker.package == 'foo.bar'

    def test_config(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.config == {}

    def test_logger_name(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.logger is None

    def test_arg_parser(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.arg_parser is None

    def test_worker_func(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.worker_func is None

    def test_success(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.success is None

    def test_failure(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.failure is None

    def test_parsed_args(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker._parsed_args is None

    def test_context(self):
        worker = NowcastWorker('worker_name', 'description')
        assert isinstance(worker._context, zmq.Context)

    def test_socket(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker._socket is None


class TestInitCli:
    """Unit test for NowcastWorker.init_cli method.
    """
    def test_debug_arg(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        assert isinstance(
            worker.arg_parser._get_option_tuples('--debug')[0][0],
            argparse._StoreTrueAction)


class TestAddArgument:
    """Unit test for NowcastWorker.add_argument method.
    """
    def test_add_argument(self):
        """add_argument() wraps argparse.ArgumentParser.add_argument()
        """
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        with patch('nemo_nowcast.worker.argparse.ArgumentParser') as m_parser:
            worker.add_argument(
                '--yesterday', action='store_true',
                help="Download forecast files for previous day's date."
            )
        m_parser().add_argument.assert_called_once_with(
            '--yesterday', action='store_true',
            help="Download forecast files for previous day's date."
        )


@patch('nemo_nowcast.lib.load_config')
@patch('nemo_nowcast.worker.logging')
class TestNowcastWorkerRun:
    """Unit tests for NowcastWorker.run method.
    """
    def test_worker_func(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        assert worker.worker_func == m_worker_func

    def test_success_func(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        assert worker.success == m_success

    def test_failure_func(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        assert worker.failure== m_failure

    def test_parse_args(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        worker.arg_parser.parse_args.assert_called_once_with()

    def test_config(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        assert worker.config == m_load_config()

    def test_logging_config(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        m_logging.config.dictConfig.assert_called_once_with(
            worker.config['logging'])

    def test_debug_mode_console_logging(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args', debug=True)
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        m_console_handler = Mock(name='m_console_handler')
        m_console_handler.name = 'console'
        m_logging.getLogger().handlers = [m_console_handler]
        worker.run(m_worker_func, m_success, m_failure)
        m_console_handler.setLevel.assert_called_once_with(m_logging.DEBUG)

    def test_logging_info(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        assert worker.logger.info.call_count == 2

    def test_init_zmq_interface(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        worker._init_zmq_interface.assert_called_once_with()

    def test_install_signal_handlers(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        worker._install_signal_handlers.assert_called_once_with()

    def test_do_work(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        m_worker_func = Mock(name='worker_func')
        m_success = Mock(name='success')
        m_failure = Mock(name='failure')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run(m_worker_func, m_success, m_failure)
        assert worker._do_work.call_count == 1


class TestInitZmqInterface:
    """Unit testss for NowcastWorker._init_zmq_interface method.
    """
    def test_debug_mode(self):
        worker = NowcastWorker('worker_name', 'description')
        worker._parsed_args = Mock(debug=True)
        worker.logger = Mock(name='logger')
        worker._context = Mock(name='context')
        worker._init_zmq_interface()
        assert worker.logger.debug.call_count == 1
        assert not worker._context.socket.called

    def test_socket(self):
        worker = NowcastWorker('worker_name', 'description')
        worker._parsed_args = Mock(debug=False)
        worker.logger = Mock(name='logger')
        worker._context = Mock(name='context')
        worker.config = {
            'zmq': {'server': 'example.com', 'ports': {'workers': 4343}}}
        worker._init_zmq_interface()
        # noinspection PyUnresolvedReferences
        worker._context.socket.assert_called_once_with(zmq.REQ)
        worker._socket.connect.assert_called_once_with('tcp://example.com:4343')
        assert worker.logger.info.call_count == 1


@pytest.mark.parametrize('i, sig', [
    (0, signal.SIGINT),
    (1, signal.SIGTERM),
])
class TestInstallSignalHandlers:
    """Unit tests for NowcastWorker._install_signal_handlers method.
    """
    def test_signal_handlers(self, i, sig):
        worker = NowcastWorker('worker_name', 'description')
        with patch('nemo_nowcast.worker.signal.signal') as m_signal:
            worker._install_signal_handlers()
        args, kwargs = m_signal.call_args_list[i]
        assert args[0] == sig


class TestDoWork:
    """Unit tests for NowcastWorker._do_work method.
    """
    def test_worker_func(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker.worker_func = Mock(name='worker_func')
        worker.success = Mock(name='success_func')
        worker._do_work()
        worker.worker_func.assert_called_once_with(
            worker._parsed_args, worker.config, worker.tell_manager)

    def test_success_func(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker.worker_func = Mock(name='worker_func')
        worker.success = Mock(name='success_func')
        worker._do_work()
        worker.success.assert_called_once_with(worker._parsed_args)

    def test_success_tell_manager(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker.worker_func = Mock(name='worker_func', return_value='checklist')
        worker.success = Mock(name='success_func', return_value='success')
        worker._do_work()
        # noinspection PyUnresolvedReferences
        worker.tell_manager.assert_called_once_with('success', 'checklist')

    def test_failure_func(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker.worker_func = Mock(name='worker_func', side_effect=WorkerError)
        worker.failure = Mock(name='failure_func')
        worker._do_work()
        worker.failure.assert_called_once_with(worker._parsed_args)

    def test_failure_tell_manager(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker.worker_func = Mock(name='worker_func', side_effect=WorkerError)
        worker.failure = Mock(name='failure_func', return_value='failure')
        worker._do_work()
        # noinspection PyUnresolvedReferences
        worker.tell_manager.assert_called_once_with('failure')

    def test_system_exit_context_destroy(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.init_cli()
        worker.logger = Mock(name='logger')
        worker._context = Mock(name='context')
        worker.worker_func = Mock(name='worker_func', side_effect=SystemExit)
        worker._do_work()
        assert worker._context.destroy.call_count == 1

    def test_logger_critical_unhandled_exception(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker._context = Mock(name='context')
        worker.worker_func = Mock(name='worker_func', side_effect=Exception)
        worker._do_work()
        worker.logger.critical.assert_called_once_with(
            'unhandled exception:', exc_info=True)

    def test_crash_tell_manager(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.logger = Mock(name='logger')
        worker.tell_manager = Mock(name='tell_manager')
        worker.worker_func = Mock(name='worker_func', side_effect=Exception)
        worker._do_work()
        # noinspection PyUnresolvedReferences
        worker.tell_manager.assert_called_once_with('crash')

    def test_logger_debug_task_completed(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.logger = Mock(name='logger')
        worker._context = Mock(name='context')
        worker.worker_func = Mock(name='worker_func', side_effect=SystemExit)
        worker._do_work()
        worker.logger.debug.assert_called_once_with(
            'task completed; shutting down')


class TestTellManager:
    """Unit tests for NowcastWorker._tell_manager method.
    """
    def test_unregistered_worker(self):
        worker = NowcastWorker('test_worker', 'description')
        worker._parsed_args = Mock(debug=True)
        worker.logger = Mock(name='logger')
        worker.config = {
            'config_file': 'nowcast.yaml',
            'message registry': {
                'workers': {
        }}}
        with pytest.raises(WorkerError):
            payload = worker.tell_manager('success', 'payload')

    def test_unregistered_worker_message_type(self):
        worker = NowcastWorker('test_worker', 'description')
        worker._parsed_args = Mock(debug=True)
        worker.logger = Mock(name='logger')
        worker.config = {
            'config_file': 'nowcast.yaml',
            'message registry': {
                'workers': {
                    'test_worker': {
                        'success': 'successful test'}
        }}}
        with pytest.raises(WorkerError):
            payload = worker.tell_manager('failure')

    def test_debug_mode(self):
        worker = NowcastWorker('test_worker', 'description')
        worker._parsed_args = Mock(debug=True)
        worker.logger = Mock(name='logger')
        worker.config = {
            'message registry': {
                'workers': {
                    'test_worker': {
                        'success': 'successful test'}
        }}}
        response_payload = worker.tell_manager('success', 'payload')
        assert worker.logger.debug.call_count == 1
        assert response_payload is None

    @patch('nemo_nowcast.lib.deserialize_message')
    @patch('nemo_nowcast.lib.serialize_message')
    def test_tell_manager(self, m_lsm, m_ldm):
        worker = NowcastWorker('test_worker', 'description')
        worker._parsed_args = Mock(debug=False)
        worker._socket = Mock(name='_socket')
        worker.logger = Mock(name='logger')
        worker.config = {
            'message registry': {
                'manager': {'ack': 'message acknowledged'},
                'workers': {
                    'test_worker': {
                        'success': 'successful test'}
        }}}
        message = namedtuple('Message', 'source, type, payload')
        m_ldm.return_value = message(source='manager', type='ack', payload=None)
        response_payload = worker.tell_manager('success', 'payload')
        worker._socket.send_string.assert_called_once_with(m_lsm())
        worker._socket.recv_string.assert_called_once_with()
        assert worker.logger.debug.call_count == 2
        assert response_payload == m_ldm()

    @patch('nemo_nowcast.lib.deserialize_message')
    @patch('nemo_nowcast.lib.serialize_message')
    def test_unregistered_manager_message_type(self, m_lsm, m_ldm):
        worker = NowcastWorker('test_worker', 'description')
        worker._parsed_args = Mock(debug=False)
        worker._socket = Mock(name='_socket')
        worker.logger = Mock(name='logger')
        worker.config = {
            'config_file': 'nowcast.yaml',
            'message registry': {
                'manager': {'ack': 'message acknowledged'},
                'workers': {
                    'test_worker': {
                        'success': 'successful test'}
        }}}
        message = namedtuple('Message', 'source, type, payload')
        m_ldm.return_value = message(source='manager', type='foo', payload=None)
        with pytest.raises(WorkerError):
            response_payload = worker.tell_manager('success', 'payload')
