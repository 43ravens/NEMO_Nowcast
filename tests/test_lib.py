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
from unittest.mock import mock_open, patch

import pytest
import yaml

from nemo_nowcast import lib


class TestBasicArgParser:
    """Unit tests for lib.basic_arg_parser function.
    """
    def test_usage_cmd(self):
        parser = lib.basic_arg_parser('message_broker')
        expected = 'python -m nemo_nowcast.message_broker'
        assert parser.prog == expected

    def test_default_no_description(self):
        parser = lib.basic_arg_parser('module_name')
        assert parser.description is None

    def test_description(self):
        parser = lib.basic_arg_parser('module_name', description='description')
        assert parser.description == 'description'

    def test_default_add_help(self):
        parser = lib.basic_arg_parser('module_name')
        assert isinstance(parser._optionals._actions[0], argparse._HelpAction)

    def test_no_help(self):
        parser = lib.basic_arg_parser('module_name', add_help=False)
        assert not isinstance(
            parser._optionals._actions[0], argparse._HelpAction)

    def test_config_file_arg(self):
        parser = lib.basic_arg_parser('module_name')
        assert parser._positionals._actions[1].dest == 'config_file'


class TestLoadConfig:
    """Unit tests for lib.load_config functions.
    """
    def test_load_config(self):
        m_open = mock_open(read_data='foo: bar')
        with patch('nemo_nowcast.lib.open', m_open):
            config = lib.load_config('nowcast.yaml')
        assert config['foo'] == 'bar'

    def test_config_file_in_config(self):
        m_open = mock_open(read_data='foo: bar')
        with patch('nemo_nowcast.lib.open', m_open):
            config = lib.load_config('nowcast.yaml')
        assert config['config_file'] == 'nowcast.yaml'


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
