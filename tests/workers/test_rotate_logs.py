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

"""Unit tests for nemo_nowcast.workers.rotate_logs module.
"""
import logging.handlers
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from nemo_nowcast.workers import rotate_logs


@patch('nemo_nowcast.workers.rotate_logs.NowcastWorker')
class TestMain:
    """Unit tests for main function.
    """
    def test_instantiate_worker(self, m_worker):
        rotate_logs.main()
        args, kwargs = m_worker.call_args
        assert args == ('rotate_logs',)
        assert 'description' in kwargs
        assert 'package' in kwargs

    def test_init_cli(self, m_worker):
        rotate_logs.main()
        m_worker().init_cli.assert_called_once_with()

    def test_run_worker(self, m_worker):
        rotate_logs.main()
        args, kwargs = m_worker().run.call_args
        expected = (
            rotate_logs.rotate_logs, rotate_logs.success, rotate_logs.failure)
        assert args == expected


@patch('nemo_nowcast.workers.rotate_logs.logger')
class TestSuccess:
    """Unit tests for success function.
    """
    def test_success_log_info(self, m_logger):
        parsed_args = SimpleNamespace()
        rotate_logs.success(parsed_args)
        assert m_logger.info.called

    def test_success_msg_type(self, m_logger):
        parsed_args = SimpleNamespace()
        msg_type = rotate_logs.success(parsed_args)
        assert msg_type == 'success'


@patch('nemo_nowcast.workers.rotate_logs.logger')
class TestFailure:
    """Unit tests for failure function.
    """
    def test_failure_log_critical(self, m_logger):
        parsed_args = SimpleNamespace()
        rotate_logs.failure(parsed_args)
        assert m_logger.critical.called

    def test_failure_msg_type(self, m_logger):
        parsed_args = SimpleNamespace()
        msg_type = rotate_logs.failure(parsed_args)
        assert msg_type == 'failure'


@pytest.mark.parametrize('config', [
    {'logging': {}},
    {'logging': {
        'aggregator': {},
        'publisher': {
            'handlers': {},
        }}},
])
@patch('nemo_nowcast.workers.rotate_logs.logging.config.dictConfig')
@patch('nemo_nowcast.workers.rotate_logs.logger')
class TestRotateLogs:
    """Unit tests for rotate_logs function.
    """

    def test_distributed_logging(self, m_logger, m_dictConfig, config):
        m_logger.root.handlers = []
        parsed_args = SimpleNamespace()
        rotate_logs.rotate_logs(parsed_args, config)
        if 'aggregator' in config['logging']:
            m_dictConfig.assert_called_once_with(
                config['logging']['aggregator'])
        else:
            assert not m_dictConfig.called

    def test_no_handlers(self, m_logger, m_dictConfig, config):
        m_logger.root.handlers = []
        parsed_args = SimpleNamespace()
        checklist = rotate_logs.rotate_logs(parsed_args, config)
        assert checklist == []

    def test_dont_roll_timed_handler(
        self, m_logger, m_dictConfig, config, tmpdir,
    ):
        tmpfile = tmpdir.ensure('foo')
        m_logger.root.handlers = [
            logging.handlers.TimedRotatingFileHandler(tmpfile.strpath)]
        parsed_args, config = SimpleNamespace(), {'logging': {}}
        checklist = rotate_logs.rotate_logs(parsed_args, config)
        assert checklist == []

    def test_dont_roll_stream_handler(self, m_logger, m_dictConfig, config):
        m_logger.root.handlers = [logging.StreamHandler()]
        parsed_args, config = SimpleNamespace(), {'logging': {}}
        checklist = rotate_logs.rotate_logs(parsed_args, config)
        assert checklist == []

    def test_roll_rotating_handler(
        self, m_logger, m_dictConfig, config, tmpdir,
    ):
        tmpfile = tmpdir.ensure('foo')
        m_logger.root.handlers = [
            logging.handlers.RotatingFileHandler(tmpfile.strpath)]
        parsed_args, config = SimpleNamespace(), {'logging': {}}
        checklist = rotate_logs.rotate_logs(parsed_args, config)
        assert checklist == [tmpfile.strpath]
