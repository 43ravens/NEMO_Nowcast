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

"""Unit tests for nemo_nowcast.workers.awaken module.
"""
from unittest.mock import Mock, patch

from nemo_nowcast.workers import awaken


@patch("nemo_nowcast.workers.awaken.NowcastWorker")
class TestMain:
    """Unit tests for main function.
    """

    def test_instantiate_worker(self, m_worker):
        awaken.main()
        args, kwargs = m_worker.call_args
        assert args == ("awaken",)
        assert "description" in kwargs
        assert "package" in kwargs

    def test_init_cli(self, m_worker):
        awaken.main()
        m_worker().init_cli.assert_called_once_with()

    def test_run_worker(self, m_worker):
        awaken.main()
        args, kwargs = m_worker().run.call_args
        assert args == (awaken.awaken, awaken.success, awaken.failure)


class TestSuccess:
    """Unit tests for success function.
    """

    def test_success_log_info(self):
        parsed_args = Mock(awaken_time=5)
        with patch("nemo_nowcast.workers.awaken.logger") as m_logger:
            awaken.success(parsed_args)
        assert m_logger.info.called

    def test_success_msg_type(self):
        parsed_args = Mock(awaken_time=5)
        with patch("nemo_nowcast.workers.awaken.logger") as m_logger:
            msg_type = awaken.success(parsed_args)
        assert msg_type == "success"


class TestFailure:
    """Unit tests for failure function.
    """

    def test_failure_log_critical(self):
        parsed_args = Mock(awaken_time=5)
        with patch("nemo_nowcast.workers.awaken.logger") as m_logger:
            awaken.failure(parsed_args)
        assert m_logger.critical.called

    def test_failure_msg_type(self):
        parsed_args = Mock(awaken_time=5)
        with patch("nemo_nowcast.workers.awaken.logger") as m_logger:
            msg_type = awaken.failure(parsed_args)
        assert msg_type == "failure"


class TestAwaken:
    """Unit tests for awaken function.
    """

    def test_example(self):
        parsed_args = Mock(awaken_time=5)
        config = {}
        checklist = awaken.awaken(parsed_args, config)
        assert checklist == {"awoke": True}
