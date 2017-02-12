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

"""Unit tests for nemo_nowcast.log_aggregator module.
"""
import logging
import signal
from unittest.mock import (
    call,
    Mock,
    patch,
)

import pytest
import zmq

from nemo_nowcast import log_aggregator


@patch('nemo_nowcast.log_aggregator.CommandLineInterface')
@patch('nemo_nowcast.log_aggregator.Config')
@patch('nemo_nowcast.log_aggregator._configure_logging')
@patch('nemo_nowcast.log_aggregator.logging')
@patch('nemo_nowcast.log_aggregator.run')
class TestMain:
    """Unit tests for log_aggregator.main function.
    """
    def test_commandline_interface(
        self, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        log_aggregator.main()
        args, kwargs = m_cli.call_args_list[0]
        assert args[0] == 'log_aggregator'
        assert 'package' in kwargs
        assert 'description' in kwargs
        m_cli.build_parser.asser_called_once_with()

    def test_cli_parser(
        self, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        log_aggregator.main()
        m_cli().parser.parse_args.assert_called_once_with()

    def test_config_load(
        self, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        log_aggregator.main()
        m_config().load.assert_called_once_with('nowcast.yaml')

    def test_logging_config(
        self, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        log_aggregator.main()
        m_config_logging.assert_called_once_with(m_config())

    @patch('nemo_nowcast.log_aggregator.logger')
    def test_logging_info(
        self, m_logger, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        log_aggregator.main()
        assert m_logger.info.call_count == 2

    def test_run(
        self, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        log_aggregator.main()
        m_run.assert_called_once_with(m_config())


@patch('nemo_nowcast.log_aggregator.logging.config')
class TestConfigureLogging:
    """Unit tests for log_aggregator._configure_logging function.
    """
    config = {'logging': {'aggregator': {'handlers': {'info_text': {
        'class': 'logging.handlers.RotatingFileHandler',
        'backupCount': 7,
    }}}}}

    def test_change_rotating_logger_handler_to_watched(self, m_logging_config):
        log_aggregator._configure_logging(self.config)
        handler = (
            self.config['logging']['aggregator']['handlers']['info_text'])
        assert handler['class'] == 'logging.handlers.WatchedFileHandler'
        assert 'backupCount' not in handler

    def test_logging_configure_dictConfig(self, m_logging_config):
        log_aggregator._configure_logging(self.config)
        m_logging_config.dictConfig.assert_called_once_with(
            self.config['logging']['aggregator'])


@patch('nemo_nowcast.log_aggregator.context')
@patch('nemo_nowcast.log_aggregator._install_signal_handlers')
@patch('nemo_nowcast.log_aggregator._process_messages')
class TestRun:
    """Unit tests for log_aggregator.run function.
    """
    def test_manager_port(self, m_proc_msgs, m_ish, m_context):
        config = {'zmq': {
            'host': 'localhost',
            'ports': {'logging': {'manager': 4343}}}}
        log_aggregator.run(config)
        m_context.socket(zmq.SUB).connect.assert_called_once_with(
            'tcp://localhost:4343')

    def test_local_worker_ports_list(self, m_proc_msgs, m_ish, m_context):
        config = {'zmq': {
            'host': 'localhost',
            'ports': {'logging': {'workers': [4345, 4346]}}}}
        log_aggregator.run(config)
        assert m_context.socket(zmq.SUB).connect.call_args_list == [
            call('tcp://localhost:4345'),
            call('tcp://localhost:4346'),
        ]

    def test_remote_worker(self, m_proc_msgs, m_ish, m_context):
        config = {'zmq': {
            'host': 'localhost',
            'ports': {'logging': {'manager': 'salish:4348'}}}}
        log_aggregator.run(config)
        m_context.socket(zmq.SUB).connect.assert_called_once_with(
            'tcp://salish:4348')

    def test_install_signal_handlers(self, m_proc_msgs, m_ish, m_context):
        config = {'zmq': {
            'host': 'localhost',
            'ports': {'logging': {'worker': 4343}}}}
        log_aggregator.run(config)
        m_ish.assert_called_once_with(m_context.socket())

    def test_process_messages(self, m_proc_msgs, m_ish, m_context):
        config = {'zmq': {
            'host': 'localhost',
            'ports': {'logging': {'worker': 4343}}}}
        log_aggregator.run(config)
        m_proc_msgs.assert_called_once_with(m_context.socket())


@patch('nemo_nowcast.log_aggregator.zmq.Socket', spec=zmq.Socket)
@patch('nemo_nowcast.log_aggregator.logger')
class TestLogMessages:
    """Unit test for log_aggregator._log_messages function.
    """
    def test_log_messages(self, m_logger, m_socket):
        m_socket.recv_multipart.return_value = [b'worker_name.INFO', b'message']
        log_aggregator._log_messages(m_socket)
        m_logger.log.assert_called_once_with(
            logging.INFO, 'message', extra={'logger_name': 'worker_name'})


@pytest.mark.parametrize('i, sig', [
    (0, signal.SIGHUP),
    (1, signal.SIGINT),
    (2, signal.SIGTERM),
])
class TestInstallSignalHandlers:
    """Unit tests for log_aggregator._install_signal_handlers function.
    """
    def test_signal_handlers(self, i, sig):
        with patch('nemo_nowcast.log_aggregator.signal.signal') as m_signal:
            log_aggregator._install_signal_handlers(Mock(name='socket'))
        args, kwargs = m_signal.call_args_list[i]
        assert args[0] == sig
