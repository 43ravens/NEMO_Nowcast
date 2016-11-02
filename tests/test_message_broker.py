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

"""Unit tests for nemo_nowcast.message_broker module.
"""
import signal
from unittest.mock import (
    call,
    Mock,
    patch,
)

import pytest
import zmq

from nemo_nowcast import message_broker


@patch('nemo_nowcast.message_broker.logging')
@patch('nemo_nowcast.message_broker.Config')
@patch('nemo_nowcast.message_broker.CommandLineInterface')
@patch('nemo_nowcast.message_broker.run')
class TestMain:
    """Unit tests for message_broker.main function.
    """
    def test_commandline_interface(self, m_run, m_cli, m_config, m_logging):
        message_broker.main()
        args, kwargs = m_cli.call_args_list[0]
        assert args[0] == 'message_broker'
        assert 'package' in kwargs
        assert 'description' in kwargs
        m_cli.build_parser.asser_called_once_with()

    def test_cli_parser(self, m_run, m_cli, m_config, m_logging):
        message_broker.main()
        m_cli().parser.parse_args.assert_called_once_with()

    def test_config_load(self, m_run, m_cli, m_config, m_logging):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        message_broker.main()
        m_config().load.assert_called_once_with('nowcast.yaml')

    def test_change_rotating_logger_handler_to_watched(
        self, m_run, m_cli, m_config, m_logging
    ):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        m_config().__getitem__().__getitem__.return_value = {
            'info_text': {
                'class': 'logging.handlers.RotatingFileHandler',
                'backupCount': 7,
        }}
        message_broker.main()
        handler = m_config().__getitem__().__getitem__()['info_text']
        assert handler['class'] == 'logging.handlers.WatchedFileHandler'
        assert 'backupCount' not in handler
        m_config().load.assert_called_once_with('nowcast.yaml')

    @patch('nemo_nowcast.message_broker.logger')
    def test_logging_info(self, m_logger, m_run, m_cli, m_config, m_logging):
        m_cli.parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        m_config().load.return_value = {'logging': {}}
        message_broker.main()
        m_logging.config.dictConfig.assert_called_once_with(
            m_config().__getitem__())
        assert m_logger.info.call_count == 2

    def test_run(self, m_run, m_cli, m_config, m_logging):
        m_cli.parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        message_broker.main()
        m_run.assert_called_once_with(m_config())


@patch('nemo_nowcast.message_broker.logger')
@patch('nemo_nowcast.message_broker._install_signal_handlers')
@patch('nemo_nowcast.message_broker._bind_zmq_sockets')
@patch('nemo_nowcast.message_broker.zmq.device')
class TestRun:
    """Unit tests for message_broker.run function.
    """
    def test_zmq_device(self, m_zmq_device, m_bzs, m_ish, m_logger):
        m_bzs.return_value = 'worker_socket', 'manager_socket'
        config = {}
        message_broker.run(config)
        m_zmq_device.assert_called_once_with(
            zmq.QUEUE, 'worker_socket', 'manager_socket')


@patch('nemo_nowcast.message_broker.context')
class TestBindZmqSockets:
    """Unit tests for message_broker._bind_zmq_sockets function.
    """
    def test_sockets(self, m_context):
        config = {
            'zmq': {'ports': {'workers': 4343, 'manager': 6665}}
        }
        worker_socket, manager_socket = message_broker._bind_zmq_sockets(config)
        assert worker_socket == m_context.socket(zmq.ROUTER)
        assert manager_socket == m_context.socket(zmq.DEALER)

    @patch('nemo_nowcast.message_broker.logger')
    def test_ports(self, m_logger, m_context):
        config = {
            'zmq': {'ports': {'workers': 4343, 'manager': 6666}}
        }
        worker_socket, manager_socket = message_broker._bind_zmq_sockets(config)
        assert worker_socket.bind.call_args_list[0] == call('tcp://*:4343')
        assert manager_socket.bind.call_args_list[1] == call('tcp://*:6666')
        assert m_logger.info.call_count == 2


@pytest.mark.parametrize('i, sig', [
    (0, signal.SIGHUP),
    (1, signal.SIGINT),
    (2, signal.SIGTERM),
])
class TestInstallSignalHandlers:
    """Unit tests for message_broker._install_signal_handlers function.
    """
    def test_signal_handlers(self, i, sig):
         with patch('nemo_nowcast.message_broker.signal.signal') as m_signal:
            message_broker._install_signal_handlers(4343, 6666)
         args, kwargs = m_signal.call_args_list[i]
         assert args[0] == sig
