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

"""Unit tests for nemo_nowcast.next_workers module."""
import pytest

from nemo_nowcast import Message, NextWorker, next_workers


@pytest.fixture(scope="function")
def config():
    """Nowcast system config dict data structure;
    a mock for :py:attr:`nemo_nowcast.config.Config._dict`.
    """
    return {}


@pytest.fixture(scope="function")
def checklist():
    """Nowcast system state checklist dict data structure;
    a mock for :py:attr:`nemo_nowcast.manager.NowcastManager.checklist`.
    """
    return {}


class TestAfterSleep:
    """Unit tests for the after_sleep function."""

    @pytest.mark.parametrize("msg_type", ["crash", "failure"])
    def test_no_next_worker_msg_types(self, msg_type, config, checklist):
        workers = next_workers.after_sleep(
            Message("sleep", msg_type), config, checklist
        )
        assert workers == []

    def test_success_awaken_worker_next(self, config, checklist):
        workers = next_workers.after_sleep(
            Message("sleep", "success"), config, checklist
        )
        assert workers == [NextWorker("nemo_nowcast.workers.awaken")]


class TestAfterAwaken:
    """Unit tests for the after_awakenfunction."""

    @pytest.mark.parametrize("msg_type", ["crash", "failure", "success"])
    def test_no_next_worker_msg_types(self, msg_type, config, checklist):
        workers = next_workers.after_awaken(
            Message("awaken", msg_type), config, checklist
        )
        assert workers == []
