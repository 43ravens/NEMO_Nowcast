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

"""Unit tests for nemo_nowcast.workers.clear_checklist module.
"""
from types import SimpleNamespace
from unittest.mock import (
    Mock,
    patch,
)

from nemo_nowcast.workers import clear_checklist


@patch('nemo_nowcast.workers.clear_checklist.NowcastWorker')
class TestMain:
    """Unit tests for main function.
    """
    def test_instantiate_worker(self, m_worker):
        clear_checklist.main()
        args, kwargs = m_worker.call_args
        assert args == ('clear_checklist',)
        assert 'description' in kwargs
        assert 'package' in kwargs

    def test_init_cli(self, m_worker):
        clear_checklist.main()
        m_worker().init_cli.assert_called_once_with()

    def test_run_worker(self, m_worker):
        clear_checklist.main()
        args, kwargs = m_worker().run.call_args
        expected = (
            clear_checklist.clear_checklist, clear_checklist.success,
            clear_checklist.failure)
        assert args == expected


@patch('nemo_nowcast.workers.clear_checklist.logger')
class TestSuccess:
    """Unit tests for success function.
    """
    def test_success_log_info(self, m_logger):
        parsed_args = SimpleNamespace()
        clear_checklist.success(parsed_args)
        assert m_logger.info.called

    def test_success_msg_type(self, m_logger):
        parsed_args = SimpleNamespace()
        msg_type = clear_checklist.success(parsed_args)
        assert msg_type == 'success'


@patch('nemo_nowcast.workers.clear_checklist.logger')
class TestFailure:
    """Unit tests for failure function.
    """
    def test_failure_log_critical(self, m_logger):
        parsed_args = SimpleNamespace()
        clear_checklist.failure(parsed_args)
        assert m_logger.critical.called

    def test_failure_msg_type(self, m_logger):
        parsed_args = SimpleNamespace()
        msg_type = clear_checklist.failure(parsed_args)
        assert msg_type == 'failure'


@patch('nemo_nowcast.workers.clear_checklist.logger')
class TestClearChecklist:
    """Unit test for clear_checklist function.
    """
    def test_send_clear_checklist_msg(self, m_logger):
        parsed_args, config = SimpleNamespace(), {}
        m_tell_manager = Mock(name='tell_manager')
        clear_checklist.clear_checklist(parsed_args, config, m_tell_manager)
        m_tell_manager.assert_called_once_with('clear checklist')
