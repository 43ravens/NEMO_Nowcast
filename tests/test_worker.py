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
import signal
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

    def test_parsed_args(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker._parsed_args is None

    def test_context(self):
        worker = NowcastWorker('worker_name', 'description')
        assert isinstance(worker._context, zmq.Context)

    def test_socket(self):
        worker = NowcastWorker('worker_name', 'description')
        assert worker._socket is None


class TestAddArgument:
    """Unit test for NowcastWorker.add_argument method.
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


# noinspection PyUnresolvedReferences
@patch('nemo_nowcast.worker.lib.load_config')
@patch('nemo_nowcast.worker.logging')
class TestNowcastWorkerRun:
    """Unit tests for NowcastWorker.run method.
    """
    def test_parse_args(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        worker.arg_parser.parse_args.assert_called_once_with()

    def test_config(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        assert worker.config == m_load_config()

    def test_logging_config(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        m_logging.config.dictConfig.assert_called_once_with(
            worker.config['logging'])

    def test_logging_info(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        assert worker.logger.info.call_count == 2

    def test_init_zmq_interface(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        worker._init_zmq_interface.assert_called_once_with()

    def test_install_signal_handlers(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        worker._install_signal_handlers.assert_called_once_with()

    def test_do_work(self, m_logging, m_load_config):
        worker = NowcastWorker('worker_name', 'description')
        worker.arg_parser.parse_args = Mock(name='parse_args')
        worker._init_zmq_interface = Mock(name='_init_zmq_interface')
        worker._install_signal_handlers = Mock(name='_install_signal_handlers')
        worker._do_work = Mock(name='_do_work')
        worker.run()
        assert worker._do_work.call_count == 1


class TestInitZmqInterface:
    """Unit testss for NowcastWorker._init_zmq_interface method.
    """
    def test_debug_mode(self):
        worker = NowcastWorker('worker_name', 'description')
        worker._parsed_args = Mock(debug=True)
        worker.logger = Mock(name='logger')
        worker._context = Mock(name='context')
        worker._init_zmq_interface()
        assert worker.logger.debug.call_count == 1
        assert not worker._context.socket.called

    def test_socket(self):
        worker = NowcastWorker('worker_name', 'description')
        worker._parsed_args = Mock(debug=False)
        worker.logger = Mock(name='logger')
        worker._context = Mock(name='context')
        worker.config = {
            'zmq': {
                'server': 'example.com',
                'ports': {
                    'frontend': 4343}}}
        worker._init_zmq_interface()
        # noinspection PyUnresolvedReferences
        worker._context.socket.assert_called_once_with(zmq.REQ)
        worker._socket.connect.assert_called_once_with('tcp://example.com:4343')
        assert worker.logger.info.call_count == 1


@patch('nemo_nowcast.worker.signal.signal')
class TestInstallSignalHandlers:
    """Unit tests for NowcastWorker._install_signal_handlers method.
    """
    def test_sigint_handler(self, m_signal):
        worker = NowcastWorker('worker_name', 'description')
        worker._install_signal_handlers()
        args, kwargs = m_signal.call_args_list[0]
        assert args[0] == signal.SIGINT

    def test_sigterm_handler(self, m_signal):
        worker = NowcastWorker('worker_name', 'description')
        worker._install_signal_handlers()
        args, kwargs = m_signal.call_args_list[1]
        assert args[0] == signal.SIGTERM
