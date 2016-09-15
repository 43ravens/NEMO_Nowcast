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
import signal
from unittest.mock import (
    patch,
    Mock,
    mock_open,
)

import pytest
import zmq

from nemo_nowcast import (
    Config,
    manager,
    Message,
    NextWorker,
)


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
        assert mgr.config == Config()

    def test_logger(self):
        mgr = manager.NowcastManager()
        assert mgr.logger is None

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
class TestNowcastManagerSetup:
    """Unit tests for NowcastManager.setup method.
    """
    @patch('nemo_nowcast.manager.importlib')
    def test_parsed_args(self, m_importlib, m_logging):
        test_config = '''
            checklist file: nowcast_checklist.yaml
            python: python
            logging:
              handlers: []
            message registry:
              next workers module: nowcast.next_workers
        '''
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        with patch('nemo_nowcast.config.open', mock_open(read_data=test_config)):
            mgr.setup()
        assert mgr._parsed_args == mgr._cli()

    @patch('nemo_nowcast.manager.importlib')
    def test_config_load(self, m_importlib, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        mgr.config.load.assert_called_once_with(mgr._parsed_args.config_file)

    @patch('nemo_nowcast.manager.importlib')
    def test_msg_registry(self, m_importlib, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        assert mgr._msg_registry == {
            'next workers module': 'nowcast.next_workers',
            'workers': {}}

    @patch('nemo_nowcast.manager.importlib')
    def test_logger_name(self, m_importlib, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        m_logging.getLogger.assert_called_once_with('manager')

    @patch('nemo_nowcast.manager.importlib')
    def test_logging_config(self, m_importlib, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        m_logging.config.dictConfig.assert_called_once_with(
            mgr.config['logging'])

    @patch('nemo_nowcast.manager.importlib')
    def test_import_next_workers_module(self, m_importlib, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
        mgr._cli = Mock(name='_cli')
        mgr.setup()
        m_importlib.import_module.assert_called_once_with(
            'nowcast.next_workers')
        assert mgr._next_workers_module == m_importlib.import_module()

    def test_next_workers_module_import_error(self, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
        mgr._cli = Mock(name='_cli')
        with pytest.raises(ImportError):
            mgr.setup()

    @patch('nemo_nowcast.manager.importlib')
    def test_logging_info(self, m_importlib, m_logging):
        mgr = manager.NowcastManager()
        mgr.config._dict = {
            'logging': {},
            'message registry': {
                'next workers module': 'nowcast.next_workers',
                'workers': {}}}
        mgr.config.load = Mock()
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
        mgr.logger = Mock(name='logger')
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
    def test_recv_string(self):
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
        next_worker = NextWorker('nowcast.workers.next_worker')
        next_worker.launch = Mock(name='launch')
        mgr._message_handler = Mock(
            name='_message_handler', return_value=('reply', [next_worker]))
        mgr._try_messages()
        next_worker.launch.assert_called_once_with(mgr.config, mgr.name)


class TestMessageHandler:
    """Unit tests for NowcastManager._message_handler method.
    """
    def test_unregistered_worker_msg(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {}}
        mgr._handle_unregistered_worker_msg = Mock(
            name='_handle_unregistered_worker_msg')
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = Message(source='worker', type='foo', payload=None)
        reply, next_workers = mgr._message_handler(msg.serialize())
        mgr._handle_unregistered_worker_msg.assert_called_once_with(msg)
        assert reply == mgr._handle_unregistered_worker_msg()
        assert next_workers == []
        assert not mgr._log_received_msg.called

    def test_unregistered_msg_type(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {'test_worker': {}}}
        mgr._handle_unregistered_msg_type = Mock(
            name='_handle_unregistered_msg_type')
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = Message(source='test_worker', type='foo', payload=None)
        reply, next_workers = mgr._message_handler(msg.serialize())
        mgr._handle_unregistered_msg_type.assert_called_once_with(msg)
        assert reply == mgr._handle_unregistered_msg_type()
        assert next_workers == []
        assert not mgr._log_received_msg.called

    def test_clear_checklist_msg(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {
            'workers': {
                'test_worker': {
                    'clear checklist':
                        'request that manager clear system checklist'}}}
        mgr._clear_checklist = Mock(
            name='_clear_checklist', return_value='checklist cleared')
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = Message(
            source='test_worker', type='clear checklist', payload=None)
        reply, next_workers = mgr._message_handler(msg.serialize())
        assert mgr._log_received_msg.called
        mgr._clear_checklist.assert_called_once_with()
        assert reply == 'checklist cleared'
        assert next_workers == []

    def test_continue_msg(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {'test_worker': {'success': 'success'}}}
        mgr._handle_continue_msg = Mock(
            name='_handle_continue_msg',
            return_value=('ack', 'next_worker'))
        mgr._log_received_msg = Mock(name='_log_received_msg')
        msg = Message(source='test_worker', type='success', payload=None)
        reply, next_workers = mgr._message_handler(msg.serialize())
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
        msg = Message(source='worker', type='foo', payload=None)
        reply = mgr._handle_unregistered_worker_msg(msg)
        assert mgr.logger.error.call_count == 1
        assert Message.deserialize(reply) == Message(
            source='manager', type='unregistered worker')


class TestHandleUnregisteredMsgType:
    """Unit test for NowcastManager._handle_unregistered_msg_type method.
    """
    def test_handle_unregistered_msg_type(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        msg = Message(source='worker', type='foo')
        reply = mgr._handle_unregistered_msg_type(msg)
        assert mgr.logger.error.call_count == 1
        assert Message.deserialize(reply) == Message(
            source='manager', type='unregistered message type')


class TestLogReceivedMessage:
    """Unit test for NowcastManager._log_received_message method.
    """
    def test_handle_unregistered_msg_type(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr._msg_registry = {
            'workers': {'test_worker': {'success': 'worker succeeded'}}}
        msg = Message(source='test_worker', type='success')
        mgr._log_received_msg(msg)
        mgr.logger.debug.assert_called_once_with(
            'received message from test_worker: (success) worker succeeded',
            extra={'worker_msg': msg}
        )


@patch('nemo_nowcast.manager.importlib')
class TestHandleContinueMsg:
    """Unit tests for NowcastManager._handle_continue_msg method.
    """
    def test_no_checklist_update_when_no_payload(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = Message(source='test_worker', type='success')
        mgr._handle_continue_msg(msg)
        assert not mgr._update_checklist.called

    @pytest.mark.parametrize('payload', ['payload', True, False, {'foo': '43'}])
    def test_update_checklist(self, m_importlib, payload):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = Message(source='test_worker', type='success', payload=payload)
        mgr._handle_continue_msg(msg)
        mgr._update_checklist.assert_called_once_with(msg)

    def test_reload_next_workers_module(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = Message(source='test_worker', type='success')
        mgr._handle_continue_msg(msg)
        m_importlib.reload.assert_called_once_with(mgr._next_workers_module)

    def test_missing_after_worker_function(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr._msg_registry = {'next workers module': 'nowcast.next_workers'}
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(name='nowcast.next_workers', spec=[])
        msg = Message(source='test_worker', type='success')
        reply, next_workers = mgr._handle_continue_msg(msg)
        assert Message.deserialize(reply) == Message(
            source='manager', type='no after_worker function')
        assert mgr.logger.critical.call_count == 1

    def test_reply(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = Message(source='test_worker', type='success')
        reply, next_workers = mgr._handle_continue_msg(msg)
        assert Message.deserialize(reply) == Message(
            source='manager', type='ack')

    def test_next_workers(self, m_importlib):
        mgr = manager.NowcastManager()
        mgr._update_checklist = Mock(name='_update_checklist')
        mgr._next_workers_module = Mock(
            name='nowcast.next_workers', test_worker=Mock())
        msg = Message(source='test_worker', type='success', payload=None)
        reply, next_workers = mgr._handle_continue_msg(msg)
        assert next_workers == mgr._next_workers_module.after_test_worker()


class TestUpdateChecklist:
    """Unit tests for NowcastManager._update_checklist method.
    """
    def test_worker_checklist_keyerror(self):
        mgr = manager.NowcastManager()
        mgr._msg_registry = {'workers': {'test_worker': {}}}
        msg = Message(
            source='test_worker', type='success', payload={'foo': 'bar'})
        with pytest.raises(KeyError):
            mgr._update_checklist(msg)

    def test_update_existing_value(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr.checklist = {'foo': 'bar'}
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'foo'}}}
        msg = Message(source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        assert mgr.checklist['foo'] == 'baz'

    def test_keyerror_adds_key_and_value(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr.checklist = {'foo': 'bar'}
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'fop'}}}
        msg = Message(source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        assert mgr.checklist['fop'] == 'baz'

    def test_log_info_msg(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr.logger = Mock(name='logger')
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'foo'}}}
        msg = Message(source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        mgr.logger.info.assert_called_once_with(
            'checklist updated with [foo] items from test_worker worker',
            extra={'worker_msg': msg})

    def test_yaml_dump_checklist_to_disk(self):
        mgr = manager.NowcastManager()
        mgr.logger = Mock(name='logger')
        mgr.checklist = {'foo': 'bar'}
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._msg_registry = {
            'workers': {'test_worker': {'checklist key': 'foo'}}}
        msg = Message(source='test_worker', type='success', payload='baz')
        mgr._update_checklist(msg)
        mgr._write_checklist_to_disk.assert_called_once_with()


class TestClearChecklist:
    """Unit tests for NowcastManager._clear_checklist method.
    """
    def test_without_checklist_logging(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr.logger = Mock(name='logger')
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        mgr._clear_checklist()
        assert mgr.checklist == {}
        assert mgr.logger.info.call_count == 1

    def test_with_checklist_logging(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr.logger = Mock(name='logger')
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        with patch('nemo_nowcast.manager.logging') as m_logging:
            m_root = m_logging.getLogger()
            m_root.handlers = [Mock(name='checklist', level=1000)]
            m_root.handlers[0].name = 'checklist'
            mgr._clear_checklist()
        mgr.logger.log.assert_called_once_with(
            1000, "checklist:\n{'foo': 'bar'}")
        assert mgr.checklist == {}
        assert mgr.logger.info.call_count == 2

    def test_checklist_cleared_msg_type(self):
        mgr = manager.NowcastManager()
        mgr.checklist = {'foo': 'bar'}
        mgr.logger = Mock(name='logger')
        mgr._write_checklist_to_disk = Mock(name='_write_checklist_to_disk')
        reply = mgr._clear_checklist()
        assert Message.deserialize(reply) == Message(
            source='manager', type='checklist cleared')
