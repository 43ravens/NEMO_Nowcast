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

"""Unit tests for nemo_nowcast.manager module.
"""
from unittest.mock import patch

from nemo_nowcast.workers import example


@patch('nemo_nowcast.workers.example.NowcastWorker')
class TestMain:
    """Unit tests for main() function.
    """
    def test_instantiate_worker(self, m_worker):
        example.main()
        args, kwargs = m_worker.call_args
        assert args == ('example',)
        assert 'description' in kwargs
        assert 'package' in kwargs

    def test_run_worker(self, m_worker):
        example.main()
        args, kwargs = m_worker().run.call_args
        assert args == ()
