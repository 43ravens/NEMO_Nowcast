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
import argparse

import zmq

from nemo_nowcast import worker


class TestNowcastWorkerConstructor:
    """Unit tests for NowcastWorker.__init__ method.
    """
    def test_name(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert wkr.name == 'worker_name'

    def test_package_default(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert wkr.package == 'nowcast.workers'

    def test_package_specified(self):
        wkr = worker.NowcastWorker(
            'worker_name', 'description', package='foo.bar')
        assert wkr.package == 'foo.bar'

    def test_description(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert wkr.description == 'description'

    def test_config(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert wkr.config is None

    def test_logger_name(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert wkr.logger.name == 'worker_name'

    def test_arg_parser(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert isinstance(wkr.arg_parser, argparse.ArgumentParser)

    def test_add_debug_arg(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert isinstance(
            wkr.arg_parser._get_option_tuples('--debug')[0][0],
            argparse._StoreTrueAction)

    def test_context(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert isinstance(wkr._context, zmq.Context)

    def test_socket(self):
        wkr = worker.NowcastWorker('worker_name', 'description')
        assert wkr._socket is None
