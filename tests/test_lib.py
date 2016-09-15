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

import arrow
import pytest

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
