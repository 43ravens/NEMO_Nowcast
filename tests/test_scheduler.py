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

"""Unit tests for nemo_nowcast.scheduler module.
"""
import signal
from unittest.mock import (
    Mock,
    patch,
)

import pytest

from nemo_nowcast import scheduler


@patch('nemo_nowcast.scheduler.logging')
@patch('nemo_nowcast.scheduler.Config')
@patch('nemo_nowcast.scheduler.CommandLineInterface')
@patch('nemo_nowcast.scheduler._install_signal_handlers')
@patch('nemo_nowcast.scheduler.run')
class TestMain:
    """Unit tests for scheduler.main function.
    """
    def test_commandline_interface(
        self, m_run, m_ish, m_cli, m_config, m_logging,
    ):
        scheduler.main()
        args, kwargs = m_cli.call_args_list[0]
        assert args[0] == 'scheduler'
        assert 'package' in kwargs
        assert 'description' in kwargs
        m_cli().build_parser.assert_called_once_with()

    def test_cli_parser(self, m_run, m_ish, m_cli, m_config, m_logging,):
        scheduler.main()
        m_cli().parser.parse_args.assert_called_once_with()

    def test_config(self, m_run, m_ish, m_cli, m_config, m_logging):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        scheduler.main()
        m_config().load.assert_called_once_with('nowcast.yaml')

    @patch('nemo_nowcast.scheduler.logger')
    def test_logging(self, m_logger, m_run, m_ish, m_cli, m_config, m_logging):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        m_config.file = 'nowcast.yaml'
        m_config().load.return_value = {'logging': {}}
        scheduler.main()
        m_logging.config.dictConfig.assert_called_once_with(
            m_config().__getitem__())
        assert m_logger.info.call_count == 2

    def test_install_signal_handlers(self, m_run, m_ish, m_cli, m_config, m_logging,
    ):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        scheduler.main()
        m_ish.assert_called_once_with()

    def test_run(self, m_run, m_ish, m_cli, m_config, m_logging):
        m_cli().parser.parse_args.return_value = Mock(
            config_file='nowcast.yaml')
        scheduler.main()
        m_run.assert_called_once_with(m_config())


class TestPrepSchedule:
    """Unit tests for scheduler._prep_schedule function.
    """
    @pytest.mark.parametrize('config, expected', [
        ({'scheduled workers': {'schedule sleep': 10}}, 10),
        ({'scheduled workers': {}}, 60),
        ({'scheduled workers': None}, 60),
        ({}, 60),
    ])
    def test_sleep_seconds_from_config(self, config, expected):
        sleep_seconds = scheduler._prep_schedule(config)
        assert sleep_seconds == expected


class TestCreateScheduledJob:
    """Unit tests for scheduler._create_scheduled_job function.
    """
    def test_no_worker_cmd_line_opts(self):
        params = {'every': 'day', 'at': '15:43'}
        config = {'scheduled workers': {'nemo_nowcast.workers.sleep': params}}
        job = scheduler._create_scheduled_job(
            'nemo_nowcast.workers.sleep', params, config)
        expected = (
            "Every 1 day at 15:43:00 do launch("
            "{'scheduled workers': {'nemo_nowcast.workers.sleep': {")
        assert str(job).startswith(expected)

    def test_worker_cmd_line_opts(self):
        params = {
            'every': 'day', 'at': '15:43', 'cmd line opts': '--sleep-time 2'}
        config = {'scheduled workers': {'nemo_nowcast.workers.sleep': params}}
        job = scheduler._create_scheduled_job(
            'nemo_nowcast.workers.sleep', params, config)
        expected = (
            "Every 1 day at 15:43:00 do launch("
            "{'scheduled workers': {'nemo_nowcast.workers.sleep': {")
        assert str(job).startswith(expected)


@pytest.mark.parametrize('i, sig', [
    (0, signal.SIGHUP),
    (1, signal.SIGINT),
    (2, signal.SIGTERM),
])
class TestInstallSignalHandlers:
    """Unit tests for scheduler._install_signal_handlers function.
    """
    def test_signal_handlers(self, i, sig):
        with patch('nemo_nowcast.scheduler.signal.signal') as m_signal:
            scheduler._install_signal_handlers()
        args, kwargs = m_signal.call_args_list[i]
        assert args[0] == sig
