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
from unittest.mock import patch, Mock

import zmq

from nemo_nowcast import manager


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

    def test_context(self):
        mgr = manager.NowcastManager()
        assert isinstance(mgr._context, zmq.Context)

    def test_socket(self):
        mgr = manager.NowcastManager()
        assert mgr._socket is None


class TestNowcastManagerSetup:
    """Unit tests for NowcastManager.setup method.
    """
    @patch('nemo_nowcast.manager.lib.load_config')
    @patch('nemo_nowcast.manager.logging')
    def test_parsed_args(self, m_logging, m_load_config):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.logger = Mock(name='logger')
        mgr.setup()
        assert mgr._parsed_args == mgr._cli()

    @patch('nemo_nowcast.manager.lib.load_config')
    @patch('nemo_nowcast.manager.logging')
    def test_config(self, m_logging, m_load_config):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.logger = Mock(name='logger')
        mgr.setup()
        m_load_config.assert_called_once_with(mgr._parsed_args.config_file)
        assert mgr.config == m_load_config()

    @patch('nemo_nowcast.manager.lib.load_config')
    @patch('nemo_nowcast.manager.logging')
    def test_logging_config(self, m_logging, m_load_config):
        mgr = manager.NowcastManager()
        mgr._cli = Mock(name='_cli')
        mgr.logger = Mock(name='logger')
        m_load_config.return_value = {'logging': ''}
        mgr.setup()
        m_logging.config.dictConfig.assert_called_once_with(
            mgr.config['logging'])


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
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'backend': 6666}}}
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._process_messages = Mock(name='_process_messages')
        mgr._context = Mock(name='zmq_context')
        mgr.run()
        assert mgr._socket == mgr._context.socket(zmq.REP)
        mgr._socket.connect.assert_called_once_with('tcp://example.com:6666')

    def test_install_signal_handers(self):
        mgr = manager.NowcastManager()
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'backend': 6666}}}
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._process_messages = Mock(name='_process_messages')
        mgr._context = Mock(name='zmq_context')
        mgr.run()
        assert mgr._install_signal_handlers.called

    def test_process_messages(self):
        mgr = manager.NowcastManager()
        mgr.config = {
            'zmq': {'server': 'example.com', 'ports': {'backend': 6666}}}
        mgr.logger = Mock(name='logger')
        mgr._install_signal_handlers = Mock(name='_install_signal_handlers')
        mgr._process_messages = Mock(name='_process_messages')
        mgr._context = Mock(name='zmq_context')
        mgr.run()
        assert mgr._process_messages.called
