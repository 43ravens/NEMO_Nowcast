# Copyright 2016 – present Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for nemo_nowcast.message_broker module."""
import signal
from unittest.mock import call, Mock, patch

import pytest
import zmq

from nemo_nowcast import message_broker


@patch("nemo_nowcast.message_broker.CommandLineInterface")
@patch("nemo_nowcast.message_broker.Config")
@patch("nemo_nowcast.message_broker._configure_logging")
@patch("nemo_nowcast.message_broker.logging")
@patch("nemo_nowcast.message_broker.run")
class TestMain:
    """Unit tests for message_broker.main function."""

    def test_commandline_interface(
        self, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        message_broker.main()
        args, kwargs = m_cli.call_args_list[0]
        assert args[0] == "message_broker"
        assert "package" in kwargs
        assert "description" in kwargs
        m_cli.build_parser.asser_called_once_with()

    def test_cli_parser(self, m_run, m_logging, m_config_logging, m_config, m_cli):
        message_broker.main()
        m_cli().parser.parse_args.assert_called_once_with()

    def test_config_load(self, m_run, m_logging, m_config_logging, m_config, m_cli):
        m_cli().parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        message_broker.main()
        m_config().load.assert_called_once_with("nowcast.yaml")

    def test_logging_config(self, m_run, m_logging, m_config_logging, m_config, m_cli):
        message_broker.main()
        m_config_logging.assert_called_once_with(m_config())

    @patch("nemo_nowcast.message_broker.logger")
    def test_logging_info(
        self, m_logger, m_run, m_logging, m_config_logging, m_config, m_cli
    ):
        m_cli.parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        m_config().load.return_value = {"logging": {}}
        message_broker.main()
        assert m_logger.info.call_count == 3

    def test_run(self, m_run, m_logging, m_config_logging, m_config, m_cli):
        m_cli.parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        message_broker.main()
        m_run.assert_called_once_with(m_config())


@patch("nemo_nowcast.message_broker.logging.config")
class TestConfigureLogging:
    """Unit tests for message_broker._configure_logging method."""

    filesystem_logging_config = {
        "logging": {
            "handlers": {
                "info_text": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "backupCount": 7,
                }
            }
        }
    }
    zmq_logging_config = {
        "logging": {"publisher": {"handlers": {"zmq_pub": {}}}},
        "zmq": {"host": "localhost", "ports": {"logging": {"message_broker": 4347}}},
    }

    @pytest.mark.parametrize(
        "config, exp_msg",
        [
            (
                filesystem_logging_config,
                "writing logging messages to local file system",
            ),
            (zmq_logging_config, "publishing logging messages to tcp://*:4347"),
        ],
    )
    def test_msg(self, m_logging_config, config, exp_msg):
        msg = message_broker._configure_logging(config)
        assert msg == exp_msg

    @pytest.mark.parametrize("config", [filesystem_logging_config, zmq_logging_config])
    def test_logging_dictConfig(self, m_logging_config, config):
        message_broker._configure_logging(config)
        if "publisher" in config["logging"]:
            m_logging_config.dictConfig.assert_called_once_with(
                config["logging"]["publisher"]
            )
        else:
            m_logging_config.dictConfig.assert_called_once_with(config["logging"])

    @patch("nemo_nowcast.message_broker.logger")
    def test_zmq_handler_root_topic(self, m_logger, m_logging_config):
        m_handler = Mock(name="m_zmq_handler", spec=zmq.log.handlers.PUBHandler)
        m_logger.root = Mock(handlers=[m_handler])
        message_broker._configure_logging(self.zmq_logging_config)
        assert m_handler.root_topic == "message_broker"

    @patch("nemo_nowcast.message_broker.logging")
    @patch("nemo_nowcast.message_broker.logger")
    def test_zmq_handler_formatters(self, m_logger, m_logging, m_logging_config):
        m_handler = Mock(name="m_zmq_handler", spec=zmq.log.handlers.PUBHandler)
        m_logger.root = Mock(handlers=[m_handler])
        message_broker._configure_logging(self.zmq_logging_config)
        expected = {
            m_logging.DEBUG: m_logging.Formatter("%(message)s\n"),
            m_logging.INFO: m_logging.Formatter("%(message)s\n"),
            m_logging.WARNING: m_logging.Formatter("%(message)s\n"),
            m_logging.ERROR: m_logging.Formatter("%(message)s\n"),
            m_logging.CRITICAL: m_logging.Formatter("%(message)s\n"),
        }
        assert m_handler.formatters == expected

    def test_change_rotating_logger_handler_to_watched(self, m_logging_config):
        message_broker._configure_logging(self.filesystem_logging_config)
        handler = self.filesystem_logging_config["logging"]["handlers"]["info_text"]
        assert handler["class"] == "logging.handlers.WatchedFileHandler"
        assert "backupCount" not in handler


@patch("nemo_nowcast.message_broker.logger")
@patch("nemo_nowcast.message_broker._install_signal_handlers")
@patch("nemo_nowcast.message_broker._bind_zmq_sockets")
@patch("nemo_nowcast.message_broker.zmq.device")
class TestRun:
    """Unit tests for message_broker.run function."""

    def test_zmq_device(self, m_zmq_device, m_bzs, m_ish, m_logger):
        m_bzs.return_value = "worker_socket", "manager_socket"
        config = {}
        message_broker.run(config)
        m_zmq_device.assert_called_once_with(
            zmq.QUEUE, "worker_socket", "manager_socket"
        )


@patch("nemo_nowcast.message_broker.context")
class TestBindZmqSockets:
    """Unit tests for message_broker._bind_zmq_sockets function."""

    def test_sockets(self, m_context):
        config = {"zmq": {"ports": {"workers": 4343, "manager": 6665}}}
        worker_socket, manager_socket = message_broker._bind_zmq_sockets(config)
        assert worker_socket == m_context.socket(zmq.ROUTER)
        assert manager_socket == m_context.socket(zmq.DEALER)

    @patch("nemo_nowcast.message_broker.logger")
    def test_ports(self, m_logger, m_context):
        config = {"zmq": {"ports": {"workers": 4343, "manager": 6666}}}
        worker_socket, manager_socket = message_broker._bind_zmq_sockets(config)
        assert worker_socket.bind.call_args_list[0] == call("tcp://*:4343")
        assert manager_socket.bind.call_args_list[1] == call("tcp://*:6666")
        assert m_logger.info.call_count == 2


@pytest.mark.parametrize(
    "i, sig", [(0, signal.SIGHUP), (1, signal.SIGINT), (2, signal.SIGTERM)]
)
class TestInstallSignalHandlers:
    """Unit tests for message_broker._install_signal_handlers function."""

    def test_signal_handlers(self, i, sig):
        with patch("nemo_nowcast.message_broker.signal.signal") as m_signal:
            message_broker._install_signal_handlers(4343, 6666)
        args, kwargs = m_signal.call_args_list[i]
        assert args[0] == sig
