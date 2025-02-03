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

"""Unit tests for nemo_nowcast.scheduler module."""
import signal
from unittest.mock import Mock, patch

import pytest
import zmq.log.handlers

from nemo_nowcast import scheduler


@patch("nemo_nowcast.scheduler.CommandLineInterface")
@patch("nemo_nowcast.scheduler.Config")
@patch("nemo_nowcast.scheduler._configure_logging")
@patch("nemo_nowcast.scheduler.logging")
@patch("nemo_nowcast.scheduler._install_signal_handlers")
@patch("nemo_nowcast.scheduler.run")
class TestMain:
    """Unit tests for scheduler.main function."""

    def test_commandline_interface(
        self, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli
    ):
        scheduler.main()
        args, kwargs = m_cli.call_args_list[0]
        assert args[0] == "scheduler"
        assert "package" in kwargs
        assert "description" in kwargs
        m_cli().build_parser.assert_called_once_with()

    def test_cli_parser(
        self, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli
    ):
        scheduler.main()
        m_cli().parser.parse_args.assert_called_once_with()

    def test_config_load(
        self, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli
    ):
        m_cli().parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        scheduler.main()
        m_config().load.assert_called_once_with("nowcast.yaml")

    def test_logging_config(
        self, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli
    ):
        scheduler.main()
        m_config_logging.assert_called_once_with(m_config())

    @patch("nemo_nowcast.scheduler.logger")
    def test_logging_info(
        self, m_logger, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli
    ):
        m_cli().parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        m_config.file = "nowcast.yaml"
        m_config().load.return_value = {"logging": {}}
        scheduler.main()
        assert m_logger.info.call_count == 3

    def test_install_signal_handlers(
        self, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli
    ):
        m_cli().parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        scheduler.main()
        m_ish.assert_called_once_with()

    def test_run(self, m_run, m_ish, m_logging, m_config_logging, m_config, m_cli):
        m_cli().parser.parse_args.return_value = Mock(config_file="nowcast.yaml")
        scheduler.main()
        m_run.assert_called_once_with(m_config())


@patch("nemo_nowcast.scheduler.logging.config")
class TestConfigureLogging:
    """Unit tests for scheduler._configure_logging method."""

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
        "zmq": {"host": "localhost", "ports": {"logging": {"scheduler": 4347}}},
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
        msg = scheduler._configure_logging(config)
        assert msg == exp_msg

    @pytest.mark.parametrize("config", [filesystem_logging_config, zmq_logging_config])
    def test_logging_dictConfig(self, m_logging_config, config):
        scheduler._configure_logging(config)
        if "publisher" in config["logging"]:
            m_logging_config.dictConfig.assert_called_once_with(
                config["logging"]["publisher"]
            )
        else:
            m_logging_config.dictConfig.assert_called_once_with(config["logging"])

    @patch("nemo_nowcast.scheduler.logger")
    def test_zmq_handler_root_topic(self, m_logger, m_logging_config):
        m_handler = Mock(name="m_zmq_handler", spec=zmq.log.handlers.PUBHandler)
        m_logger.root = Mock(handlers=[m_handler])
        scheduler._configure_logging(self.zmq_logging_config)
        assert m_handler.root_topic == "scheduler"

    @patch("nemo_nowcast.scheduler.logging")
    @patch("nemo_nowcast.scheduler.logger")
    def test_zmq_handler_formatters(self, m_logger, m_logging, m_logging_config):
        m_handler = Mock(name="m_zmq_handler", spec=zmq.log.handlers.PUBHandler)
        m_logger.root = Mock(handlers=[m_handler])
        scheduler._configure_logging(self.zmq_logging_config)
        expected = {
            m_logging.DEBUG: m_logging.Formatter("%(message)s\n"),
            m_logging.INFO: m_logging.Formatter("%(message)s\n"),
            m_logging.WARNING: m_logging.Formatter("%(message)s\n"),
            m_logging.ERROR: m_logging.Formatter("%(message)s\n"),
            m_logging.CRITICAL: m_logging.Formatter("%(message)s\n"),
        }
        assert m_handler.formatters == expected

    def test_change_rotating_logger_handler_to_watched(self, m_logging_config):
        scheduler._configure_logging(self.filesystem_logging_config)
        handler = self.filesystem_logging_config["logging"]["handlers"]["info_text"]
        assert handler["class"] == "logging.handlers.WatchedFileHandler"
        assert "backupCount" not in handler


class TestCreateScheduledJob:
    """Unit tests for scheduler._create_scheduled_job function."""

    def test_no_worker_cmd_line_opts(self):
        params = {"every": "day", "at": "15:43"}
        config = {"scheduled workers": {"nemo_nowcast.workers.sleep": params}}
        job = scheduler._create_scheduled_job(
            "nemo_nowcast.workers.sleep", params, config
        )
        assert job.interval == 1
        assert job.unit == "days"
        assert job.job_func.args == (config, "scheduler")

    def test_worker_cmd_line_opts(self):
        params = {"every": "day", "at": "15:43", "cmd line opts": "--sleep-time 2"}
        config = {"scheduled workers": {"nemo_nowcast.workers.sleep": params}}
        job = scheduler._create_scheduled_job(
            "nemo_nowcast.workers.sleep", params, config
        )
        assert job.interval == 1
        assert job.unit == "days"
        assert job.job_func.args == (config, "scheduler")


@pytest.mark.parametrize(
    "i, sig", [(0, signal.SIGHUP), (1, signal.SIGINT), (2, signal.SIGTERM)]
)
class TestInstallSignalHandlers:
    """Unit tests for scheduler._install_signal_handlers function."""

    def test_signal_handlers(self, i, sig):
        with patch("nemo_nowcast.scheduler.signal.signal") as m_signal:
            scheduler._install_signal_handlers()
        args, kwargs = m_signal.call_args_list[i]
        assert args[0] == sig
