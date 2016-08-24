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

"""Unit tests for lib module.
"""
import argparse
from datetime import datetime
from unittest.mock import (
    Mock,
    mock_open,
    patch,
)

import arrow
import pytest
import yaml

from nemo_nowcast import lib


class TestBasicArgParser:
    """Unit tests for lib.basic_arg_parser function.
    """
    def test_usage_cmd(self):
        parser = lib.base_arg_parser('message_broker')
        expected = 'python -m nowcast.message_broker'
        assert parser.prog == expected

    def test_default_no_description(self):
        parser = lib.base_arg_parser('module_name')
        assert parser.description is None

    def test_description(self):
        parser = lib.base_arg_parser('module_name', description='description')
        assert parser.description == 'description'

    def test_default_add_help(self):
        parser = lib.base_arg_parser('module_name')
        assert isinstance(parser._optionals._actions[0], argparse._HelpAction)

    def test_no_help(self):
        parser = lib.base_arg_parser('module_name', add_help=False)
        assert not isinstance(
            parser._optionals._actions[0], argparse._HelpAction)

    def test_config_file_arg(self):
        parser = lib.base_arg_parser('module_name')
        assert parser._positionals._actions[1].dest == 'config_file'


class TestLoadConfig:
    """Unit tests for lib.load_config functions.
    """
    def test_load_config(self):
        m_open = mock_open(
            read_data=(
                'foo: bar\n'
                'checklist file: nowcast_checklist.yaml\n'
                'python: python\n'
                'logging:\n'
                '  handlers: []'))
        with patch('nemo_nowcast.lib.open', m_open):
            config = lib.load_config('nowcast.yaml')
        assert config['foo'] == 'bar'

    def test_config_file_in_config(self):
        m_open = mock_open(
            read_data=(
                'foo: bar\n'
                'checklist file: nowcast_checklist.yaml\n'
                'python: python\n'
                'logging:\n'
                '  handlers: []'))
        with patch('nemo_nowcast.lib.open', m_open):
            config = lib.load_config('nowcast.yaml')
        assert config['config_file'] == 'nowcast.yaml'

    def test_replace_checklist_file_envvar(self):
        m_open = mock_open(
            read_data=(
                'foo: bar\n'
                'checklist file: $(NOWCAST.ENV.foo)/nowcast_checklist.yaml\n'
                'python: python\n'
                'logging:\n'
                '  handlers: []'))
        with patch('nemo_nowcast.lib._replace_env', return_value='bar'):
            with patch('nemo_nowcast.lib.open', m_open):
                config = lib.load_config('nowcast.yaml')
        assert config['checklist file'] == 'bar/nowcast_checklist.yaml'

    def test_replace_python_interpreter_envvar(self):
        m_open = mock_open(
            read_data=(
                'foo: bar\n'
                'checklist file: nowcast_checklist.yaml\n'
                'python: $(NOWCAST.ENV.foo)/bin/python\n'
                'logging:\n'
                '  handlers: []'))
        with patch('nemo_nowcast.lib._replace_env', return_value='bar'):
            with patch('nemo_nowcast.lib.open', m_open):
                config = lib.load_config('nowcast.yaml')
        assert config['python'] == 'bar/bin/python'

    @patch('nemo_nowcast.lib._replace_env', return_value='bar')
    def test_replace_log_file_envvar(self, m_replace_env):
        m_open = mock_open(
            read_data=(
                'foo: bar\n'
                'checklist file: nowcast_checklist.yaml\n'
                'python: python\n'
                'logging:\n'
                '  handlers:\n'
                '    info_test:\n'
                '      filename: $(NOWCAST.ENV.foo)/nowcast.log'))
        with patch('nemo_nowcast.lib.open', m_open):
            config = lib.load_config('nowcast.yaml')
        filename = config['logging']['handlers']['info_test']['filename']
        assert filename == 'bar/nowcast.log'

    @patch('nemo_nowcast.lib._replace_env', return_value='bar')
    def test_ignore_log_stream_handler(self, m_replace_env):
        m_open = mock_open(
            read_data=(
                'foo: bar\n'
                'checklist file: nowcast_checklist.yaml\n'
                'python: python\n'
                'logging:\n'
                '  handlers:\n'
                '    console: {}'))
        with patch('nemo_nowcast.lib.open', m_open):
            config = lib.load_config('nowcast.yaml')
        assert m_replace_env.call_count == 0


class TestReplaceEnv:
    """Unit tests for lib._replace_env function.
    """
    @patch.dict('nemo_nowcast.lib.os.environ', {'foo': 'bar'})
    def test_replace_env(self):
        var = Mock(name='re_var', group=Mock(return_value='foo'))
        value = lib._replace_env(var)
        assert value == 'bar'

    def test_envvar_not_set(self):
        var = Mock(name='re_var', group=Mock(return_value='foo'))
        with pytest.raises(KeyError):
            value = lib._replace_env(var)


class TestDeserializeMessage:
    """Unit tests for lib.deserialize_message function.
    """
    @pytest.mark.parametrize('source, msg_type, payload', [
        ('manager', 'ack', None),
        ('download_weather', 'success 00', {'00 forecast': True}),
    ])
    def test_deserialize_message(self, source, msg_type, payload):
        message = yaml.dump(
            {'source': source, 'type': msg_type, 'payload': payload})
        msg = lib.deserialize_message(message)
        assert msg.source == source
        assert msg.type == msg_type
        assert msg.payload == payload


class TestSerializeMessage:
    """Unit tests for lib.serialize_message function.
    """
    @pytest.mark.parametrize('source, msg_type, payload', [
        ('manager', 'unregistered worker', None),
        ('download_weather', 'success 00', {'00 forecast': True}),
    ])
    def test_serialize_message(self, source, msg_type, payload):
        msg = lib.serialize_message(source, msg_type, payload)
        expected = {'source': source, 'type': msg_type, 'payload': payload}
        assert yaml.safe_load(msg) == expected


class TestArrowDate:
    """Unit tests for arrow_date() function.
    """
    def test_arrow_date_default_timezone(self):
        arw = lib.arrow_date('2015-07-26')
        expected = arrow.get(datetime(2015, 7, 26, 0, 0, 0), 'Canada/Pacific')
        assert arw == expected

    def test_arrow_date_timezone(self):
        arw = lib.arrow_date('2015-07-26', 'Canada/Atlantic')
        expected = arrow.get(datetime(2015, 7, 26, 0, 0, 0), 'Canada/Atlantic')
        assert arw == expected

    def test_arrow_date_parse_erroe(self):
        with pytest.raises(argparse.ArgumentTypeError):
            lib.arrow_date('205-7-261')
