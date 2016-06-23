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
from unittest.mock import (
    Mock,
    patch,
)

import zmq

from nemo_nowcast.worker import NowcastWorker


class TestNowcastWorkerConstructor:
    """Unit tests for NowcastWorker.__init__ method.
    """
    def test_name(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.name == 'worker_name'

    def test_package_default(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.package == 'nowcast.workers'

    def test_package_specified(self):
        worker = NowcastWorker('worker_name', 'description', package='foo.bar')
        assert worker.package == 'foo.bar'

    def test_description(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.description == 'description'

    def test_config(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.config is None

    def test_logger_name(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker.logger.name == 'worker_name'

    def test_arg_parser(self):
        worker = NowcastWorker('worker_name', 'description')
        assert isinstance(worker.arg_parser, argparse.ArgumentParser)

    def test_add_debug_arg(self):
        worker = NowcastWorker('worker_name', 'description')
        assert isinstance(
            worker.arg_parser._get_option_tuples('--debug')[0][0],
            argparse._StoreTrueAction)

    def test_context(self):
        worker = NowcastWorker('worker_name', 'description')
        assert isinstance(worker._context, zmq.Context)

    def test_socket(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker._socket is None


class TestAddArgument:
    """Unit test for NowcastWorker.add_argument() method.
    """
    def test_add_argument(self):
        """add_argument() wraps argparse.ArgumentParser.add_argument()
        """
        worker = NowcastWorker('worker_name', 'description')
        with patch('nemo_nowcast.worker.argparse.ArgumentParser') as m_parser:
            worker.add_argument(
                '--yesterday', action='store_true',
                help="Download forecast files for previous day's date."
            )
        m_parser().add_argument.assert_called_once_with(
            '--yesterday', action='store_true',
            help="Download forecast files for previous day's date."
        )


class TestNowcastWorkerRun:
    """Unit tests for NowcastWorker.run() method.
    """
    def test_parse_args(self):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker.run()
        worker.arg_parser.parse_args.assert_called_once_with()
