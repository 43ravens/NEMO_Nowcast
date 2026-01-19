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

"""Unit tests for nemo_nowcast.workers.sleep module."""

from unittest.mock import Mock, patch

from nemo_nowcast.workers import sleep


@patch("nemo_nowcast.workers.sleep.NowcastWorker")
class TestMain:
    """Unit tests for main function."""

    def test_instantiate_worker(self, m_worker):
        sleep.main()
        args, kwargs = m_worker.call_args
        assert args == ("sleep",)
        assert "description" in kwargs
        assert "package" in kwargs

    def test_init_cli(self, m_worker):
        sleep.main()
        m_worker().init_cli.assert_called_once_with()

    def test_add_sleep_time_arg(self, m_worker):
        sleep.main()
        worker = m_worker()
        args, kwargs = worker.cli.parser.set_defaults.call_args_list[0]
        assert kwargs["sleep_time"] == 5
        args, kwargs = worker.cli.parser.add_argument.call_args_list[0]
        assert args == ("--sleep-time",)
        assert kwargs["type"] == int
        assert "help" in kwargs

    def test_run_worker(self, m_worker):
        sleep.main()
        args, kwargs = m_worker().run.call_args
        assert args == (sleep.sleep, sleep.success, sleep.failure)


class TestSuccess:
    """Unit tests for success function."""

    def test_success_log_info(self):
        parsed_args = Mock(sleep_time=5)
        with patch("nemo_nowcast.workers.sleep.logger") as m_logger:
            sleep.success(parsed_args)
        assert m_logger.info.called
        assert m_logger.info.call_args[1]["extra"]["sleep_time"] == 5

    def test_success_msg_type(self):
        parsed_args = Mock(sleep_time=5)
        with patch("nemo_nowcast.workers.sleep.logger") as m_logger:
            msg_type = sleep.success(parsed_args)
        assert msg_type == "success"


class TestFailure:
    """Unit tests for failure function."""

    def test_failure_log_critical(self):
        parsed_args = Mock(sleep_time=5)
        with patch("nemo_nowcast.workers.sleep.logger") as m_logger:
            sleep.failure(parsed_args)
        assert m_logger.critical.called
        assert m_logger.critical.call_args[1]["extra"]["sleep_time"] == 5

    def test_failure_msg_type(self):
        parsed_args = Mock(sleep_time=5)
        with patch("nemo_nowcast.workers.sleep.logger") as m_logger:
            msg_type = sleep.failure(parsed_args)
        assert msg_type == "failure"


class TestSleep:
    """Unit tests for sleep function."""

    @patch("nemo_nowcast.workers.sleep.time.sleep")
    def test_example(self, m_sleep):
        parsed_args = Mock(sleep_time=5)
        config = {}
        checklist = sleep.sleep(parsed_args, config)
        m_sleep.assert_called_once_with(5)
        assert checklist == {"sleep time": 5}
