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

"""Unit tests for nemo_nowcast.manager module.
"""
from collections import namedtuple
import signal
from unittest.mock import (
    call,
    patch,
    Mock,
    mock_open,
)

import pytest
import yaml
import zmq

from nemo_nowcast import manager

# Message data structure
message = namedtuple('Message', 'source, type, payload')


@patch('nemo_nowcast.manager.NowcastManager')
class TestMain:
    """Unit tests for the nemo_nowcast.manager.main function.
    """
    def test_main_setup(self, m_mgr):
        manager.main()
        assert m_mgr().setup.called

    def test_main_run(self, m_mgr):
        manager.main()
        assert m_mgr().run.called


class TestNowcastManagerConstructor:
    """Unit tests for NowcastManager.__init__ method.
    """
    def test_default_name(self):
        mgr = manager.NowcastManager()
        assert mgr.name == 'manager'

    def test_specified_name(self):
        mgr = manager.NowcastManager('foo')
        assert mgr.name == 'foo'

    def test_config(self):
        mgr = manager.NowcastManager()
        assert mgr.config is None

    def test_logger_name(self):
        mgr = manager.NowcastManager()
        assert mgr.logger.name == 'manager'

    def test_checklist_logger_name(self):
        mgr = manager.NowcastManager()
        assert mgr.checklist_logger.name == 'checklist'

    def test_checklist(self):
        mgr = manager.NowcastManager()
        assert mgr.checklist == {}

    def test_parsed_args(self):
        mgr = manager.NowcastManager()
        assert mgr._parsed_args is None

    def test_msg_registry(self):
        mgr = manager.NowcastManager()
        assert mgr._msg_registry is None

    def test_next_workers_module(self):
        mgr = manager.NowcastManager()
        assert mgr._next_workers_module is None

    def test_context(self):
        mgr = manager.NowcastManager()
        assert isinstance(mgr._context, zmq.Context)

    def test_socket(self):
        mgr = manager.NowcastManager()
        assert mgr._socket is None


@patch('nemo_nowcast.manager.logging')
@patch('nemo_nowcast.manager.lib.load_config')
class TestNowcastManagerSetup:
    """Unit tests for NowcastManager.setup method.
    """

    @patch('nemo_nowcast.manager.importlib')
    def test_parsed_args(self, m_load_config, m_logging, m_importlib):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        assert mgr._parsed_args == mgr._cli()

    @patch('nemo_nowcast.manager.importlib')
    def test_config(self, m_importlib, m_load_config, m_logging):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        m_load_config.assert_called_once_with(mgr._parsed_args.config_file)
        assert mgr.config == m_load_config()

    @patch('nemo_nowcast.manager.importlib')
    def test_msg_registry(self, m_importlib, m_load_config, m_logging):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        m_load_config.return_value = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.setup()
        m_load_config.assert_called_once_with(mgr._parsed_args.config_file)
        assert mgr._msg_registry == {
            'next workers module': 'nowcast.next_workers',
            'workers': {}}

    @patch('nemo_nowcast.manager.importlib')
    def test_logging_config(self, m_importlib, m_load_config, m_logging):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        m_logging.config.dictConfig.assert_called_once_with(
            mgr.config['logging'])

    @patch('nemo_nowcast.manager.importlib')
    def test_import_next_workers_module(
        self, m_importlib, m_load_config, m_logging,
    ):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        m_load_config.return_value = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.setup()
        m_importlib.import_module.assert_called_once_with(
            'nowcast.next_workers')
        assert mgr._next_workers_module == m_importlib.import_module()

    def test_next_workers_module_import_error(self, m_load_config, m_logging):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        m_load_config.return_value = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        with pytest.raises(ImportError):
            mgr.setup()

    @patch('nemo_nowcast.manager.importlib')
    def test_logging_info(self, m_importlib, m_load_config, m_logging):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        assert mgr.logger.info.call_count == 3


class TestCli:
    """Unit tests for NowcastManager._cli method.
    """
    def test_config_file(self):
        mgr = manager.NowcastManager()
        parsed_args = mgr._cli(['foo.yaml'])
        assert parsed_args.config_file == 'foo.yaml'

    def test_ignore_checklist_default(self):
        mgr = manager.NowcastManager()
        parsed_args = mgr._cli(['foo.yaml'])
        assert not parsed_args.ignore_checklist

    def test_ignore_checklist(self):
        mgr = manager.NowcastManager()
        parsed_args = mgr._cli(['foo.yaml', '--ignore-checklist'])
        assert parsed_args.ignore_checklist


class TestNowcastManagerRun:
    """Unit tests for NowcastManager.run method.
    """
    def test_socket(self):
        mgr = manager.NowcastManager()
        mgr._parsed_args = Mock(config_file='foo.yaml', ignore_checklist=True)
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'manager': 6666}}}
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._process_messages = Mock(name='_process_messages')
        mgr._context = Mock(name='zmq_context')
        mgr.run()
        assert mgr._socket == mgr._context.socket(zmq.REP)
        mgr._socket.connect.assert_called_once_with('tcp://example.com:6666')

    def test_install_signal_handers(self):
        mgr = manager.NowcastManager()
        mgr._parsed_args = Mock(config_file='foo.yaml', ignore_checklist=True)
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'manager': 6666}}}
        mgr._context = Mock(name='zmq_context')
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._process_messages = Mock(name='_process_messages')
        mgr.run()
        assert mgr._install_signal_handlers.called

    def test_load_checklist(self):
        mgr = manager.NowcastManager()
        mgr._parsed_args = Mock(config_file='foo.yaml', ignore_checklist=False)
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'manager': 6666}}}
        mgr._context = Mock(name='zmq_context')
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._load_checklist = Mock(name='_load_checklist')
        mgr._process_messages = Mock(name='_process_messages')
        mgr.run()
        assert mgr._load_checklist.called

    def test_process_messages(self):
        mgr = manager.NowcastManager()
        mgr._parsed_args = Mock(config_file='foo.yaml', ignore_checklist=True)
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'manager': 6666}}}
        mgr._context = Mock(name='zmq_context')
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._process_messages = Mock(name='_process_messages')
        mgr.run()
        assert mgr._process_messages.called


@pytest.mark.parametrize('i, sig', [
    (0, signal.SIGHUP),
    (1, signal.SIGINT),
    (2, signal.SIGTERM),
])
class TestInstallSignalHandlers:
    """Unit tests for NowcastManager._install_signal_handlers method.
    """
    def test_signal_handlers(self, i, sig):
        mgr = manager.NowcastManager()
        with patch('nemo_nowcast.manager.signal.signal') as m_signal:
            mgr._install_signal_handlers('example.com', 4343)
        args, kwargs = m_signal.call_args_list[i]
        assert args[0] == sig


class TestLoadChecklist:
    """Unit tests for NowcastManager._load_checklist method.
    """
    def test_load_checklist(self):
        mgr = manager.NowcastManager()
        p_open = patch('nemo_nowcast.manager.open', mock_open(), create=True)
        mgr.config = {'checklist file': 'nowcast_checklist.yaml'}
        with p_open as m_open:
            mgr._load_checklist()
        m_open.assert_called_once_with('nowcast_checklist.yaml', 'rt')

    def test_load_checklist_filenotfounderror(self):
        mgr = manager.NowcastManager()
        mgr.config = {'checklist file': 'nowcast_checklist.yaml'}
        mgr.logger = Mock(name='logger')
        mgr._load_checklist()
        mgr.logger.warning.assert_called_with('running with empty checklist')


class TestTryMessages:
    """Unit tests for NowcastManager._try_messages method.
    """
    def test_rev_string(self):
        mgr = manager.NowcastManager()
        mgr._socket = Mock(name='_socket')
        mgr._message_handler = Mock(
            name='_message_handler', return_value=('reply', []))
        mgr._try_messages()
        mgr._socket.recv_string.assert_called_once_with()

    def test_handle_message(self):
        mgr = manager.NowcastManager()
        mgr._socket = Mock(name='_socket')
        mgr._message_handler = Mock(
            name='_message_handler', return_value=('reply', []))
        mgr._try_messages()
        mgr._message_handler.assert_called_once_with(mgr._socket.recv_string())

    def test_send_reply(self):
        mgr = manager.NowcastManager()
        mgr._socket = Mock(name='_socket')
        mgr._message_handler = Mock(
            name='_message_handler', return_value=('reply', []))
        mgr._try_messages()
        mgr._socket.send_string.assert_called_once_with('reply')

    def test_launch_next_workers(self):
        mgr = manager.NowcastManager()
        mgr._socket = Mock(name='_socket')
        mgr._message_handler = Mock(
            name='_message_handler',
            return_value=('reply', [('test_worker', ('args',))]))
        mgr._launch_worker = Mock(name='_launch_worker')
        mgr._try_messages()
        mgr._launch_worker.assert_called_once_with('test_worker', ('args',))



class TestMessageHandler:
    """Unit tests for NowcastManager._message_handler method.
    """
    def test_unregistered_worker_msg(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {}}
        mgr._handle_unregistered_worker_msg = Mock(
            name='_handle_unregistered_worker_msg')
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = message(source='worker', type='foo', payload=None)
        msg_dict = {
            'source': msg.source, 'type': msg.type, 'payload': msg.payload}
        reply, next_steps = mgr._message_handler(yaml.dump(msg_dict))
        mgr._handle_unregistered_worker_msg.assert_called_once_with(msg)
        assert reply == mgr._handle_unregistered_worker_msg()
        assert next_steps == []
        assert not mgr._log_received_msg.called

    def test_unregistered_msg_type(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {'test_worker': {}}}
        mgr._handle_unregistered_msg_type = Mock(
            name='_handle_unregistered_msg_type')
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = message(source='test_worker', type='foo', payload=None)
        msg_dict = {
            'source': msg.source, 'type': msg.type, 'payload': msg.payload}
        reply, next_steps = mgr._message_handler(yaml.dump(msg_dict))
        mgr._handle_unregistered_msg_type.assert_called_once_with(msg)
        assert reply == mgr._handle_unregistered_msg_type()
        assert next_steps == []
        assert not mgr._log_received_msg.called

    def test_continue_msg(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {'test_worker': {'success': 'success'}}}
        mgr._handle_continue_msg = Mock(
            name='_handle_continue_msg',
            return_value=('ack', 'next_worker'))
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = message(source='test_worker', type='success', payload=None)
        msg_dict = {
            'source': msg.source, 'type': msg.type, 'payload': msg.payload}
        reply, next_workers = mgr._message_handler(yaml.dump(msg_dict))
        assert mgr._log_received_msg.called
        mgr._handle_continue_msg.assert_called_once_with(msg)
        assert reply == 'ack'
        assert next_workers == 'next_worker'


class TestHandleUnregisteredWorkerMsg:
    """Unit test for NowcastManager._handle_unregistered_worker_msg method.
    """
    def test_handle_unregistered_worker_msg(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        msg = message(source='worker', type='foo', payload=None)
        reply = mgr._handle_unregistered_worker_msg(msg)
        assert mgr.logger.error.call_count == 1
        expected = {
            'source': 'manager', 'type': 'unregistered worker',
            'payload': None}
        assert yaml.safe_load(reply) == expected


class TestHandleUnregisteredMsgType:
    """Unit test for NowcastManager._handle_unregistered_msg_type method.
    """
    def test_handle_unregistered_msg_type(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        msg = message(source='worker', type='foo', payload=None)
        reply = mgr._handle_unregistered_msg_type(msg)
        assert mgr.logger.error.call_count == 1
        expected = {
            'source': 'manager', 'type': 'unregistered message type',
            'payload': None}
        assert yaml.safe_load(reply) == expected


class TestLogReceivedMessage:
    """Unit test for NowcastManager._log_received_message method.
    """
    def test_handle_unregistered_msg_type(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr._msg_registry = {
            'workers': {'test_worker': {'success': 'worker succeeded'}}}
        msg = message(source='test_worker', type='success', payload=None)
        mgr._log_received_msg(msg)
        mgr.logger.debug.assert_called_once_with(
            'received message from test_worker: (success) worker succeeded',
            extra={'worker_msg': msg}
        )


@patch('nemo_nowcast.manager.importlib')
class TestHandleContinueMsg:
    """Unit tests for NowcastManager._handle_continue_msg method.
    """
    def test_update_checklist(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = message(source='test_worker', type='success', payload=None)
        mgr._handle_continue_msg(msg)
        mgr._update_checklist.assert_called_once_with(msg)

    def test_reload_next_workers_module(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = message(source='test_worker', type='success', payload=None)
        mgr._handle_continue_msg(msg)
        m_importlib.reload.assert_called_once_with(mgr._next_workers_module)

    def test_missing_after_worker_function(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr._msg_registry = {'next workers module': 'nowcast.next_workers'}
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(name='nowcast.next_workers', spec=[])
        msg = message(source='test_worker', type='success', payload=None)
        reply, next_workers = mgr._handle_continue_msg(msg)
        expected = {
            'source': 'manager',
            'type': 'no after_worker function',
            'payload': None}
        assert yaml.safe_load(reply) == expected
        assert mgr.logger.critical.call_count == 1

    def test_reply(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = message(source='test_worker', type='success', payload=None)
        reply, next_workers = mgr._handle_continue_msg(msg)
        expected = {'source': 'manager', 'type': 'ack', 'payload': None}
        assert yaml.safe_load(reply) == expected

    def test_next_workers(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = message(source='test_worker', type='success', payload=None)
        reply, next_workers = mgr._handle_continue_msg(msg)
        assert next_workers == mgr._next_workers_module.after_test_worker()


class TestUpdateChecklist:
    """Unit tests for NowcastManager._update_checklist method.
    """
    def test_worker_checklist_keyerror(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {'test_worker': {}}}
        msg = message(
            source='test_worker', type='success', payload={'foo': 'bar'})
        with pytest.raises(KeyError):
            mgr._update_checklist(msg)

    def test_update_existing_value(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'foo'}}}
        msg = message(
            source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        assert mgr.checklist['foo'] == 'baz'

    def test_keyerror_adds_key_and_value(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'fop'}}}
        msg = message(
            source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        assert mgr.checklist['fop'] == 'baz'

    def test_log_info_msg(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr.logger = Mock(name='logger')
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'foo'}}}
        msg = message(
            source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        mgr.logger.info.assert_called_once_with(
            'checklist updated with [foo] items from test_worker worker',
            extra={'worker_msg': msg})

    def test_yaml_dump_checklist_to_disk(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'foo'}}}
        msg = message(
            source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        mgr._write_checklist_to_disk.assert_called_once_with()


@patch('nemo_nowcast.manager.subprocess')
class TestLaunchWorker:
    """Unit tests for NowcastManager._launch_worker method.
    """
    def test_localhost(self, m_subprocess):
        mgr = manager.NowcastManager()
        mgr.config = {
            'python': 'nowcast-env/bin/python3',
            'config_file': 'nowcast.yaml',
        }
        mgr._launch_worker('nowcast.workers.test_worker', ('--debug',))
        cmd = m_subprocess.Popen.call_args_list[0]
        expected = call(
            ['nowcast-env/bin/python3', '-m', 'nowcast.workers.test_worker',
             'nowcast.yaml', '--debug'])
        assert cmd == expected

    def test_remote_host(self, m_subprocess):
        mgr = manager.NowcastManager()
        mgr.config = {
            'run': {
                'remotehost': {'python': 'nowcast-env/bin/python3',
                'config_file': 'nowcast.yaml',
        }}}
        mgr._launch_worker(
            'nowcast.workers.test_worker', ('--debug',), host='remotehost')
        cmd = m_subprocess.Popen.call_args_list[0]
        expected = call(
            ['ssh', 'remotehost',
             'nowcast-env/bin/python3', '-m', 'nowcast.workers.test_worker',
             'nowcast.yaml', '--debug'])
        assert cmd == expected

    def test_no_cmdline_args(self, m_subprocess):
        mgr = manager.NowcastManager()
        mgr.config = {
            'python': 'nowcast-env/bin/python3',
            'config_file': 'nowcast.yaml',
        }
        mgr._launch_worker('nowcast.workers.test_worker')
        cmd = m_subprocess.Popen.call_args_list[0]
        expected = call(
            ['nowcast-env/bin/python3', '-m', 'nowcast.workers.test_worker',
             'nowcast.yaml'])
        assert cmd == expected
