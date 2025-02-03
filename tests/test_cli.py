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

"""Unit tests for cli module."""
import argparse
from datetime import datetime
from unittest.mock import patch

import arrow
import pytest

from nemo_nowcast.cli import CommandLineInterface


class TestCommandLineInterface:
    """Unit tests for nemo_nowcast.cli.CommandLineInterface constructor."""

    def test_module_name(self):
        cli = CommandLineInterface("test")
        assert cli.module_name == "test"

    def test_default_package(self):
        cli = CommandLineInterface("test")
        assert cli.package == "nowcast"

    def test_package(self):
        cli = CommandLineInterface("test", package="foo")
        assert cli.package == "foo"

    def test_default_no_description(self):
        cli = CommandLineInterface("test")
        assert cli.description is None

    def test_description(self):
        cli = CommandLineInterface("test", description="foo bar baz")
        assert cli.description == "foo bar baz"

    def test_parser(self):
        cli = CommandLineInterface("test")
        assert cli.parser is None


class TestBuildParser:
    """Unit tests for nemo_nowcast.cli.CommandLineInterface.build_parser method."""

    def test_usage(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        assert cli.parser.prog == "python -m nowcast.test"

    def test_default_add_help(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        assert isinstance(cli.parser._optionals._actions[0], argparse._HelpAction)

    def test_no_help(self):
        cli = CommandLineInterface("test")
        cli.build_parser(add_help=False)
        assert not isinstance(cli.parser._optionals._actions[0], argparse._HelpAction)

    def test_config_file_arg(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        assert cli.parser._positionals._actions[1].dest == "config_file"


@patch("nemo_nowcast.cli.argparse.ArgumentParser")
class TestAddArgument:
    """Unit test for nemo_nowcast.cli.CommandLineInterface.add_argument method."""

    def test_add_argument(self, m_parser):
        """add_argument() wraps argparse.ArgumentParser.add_argument()"""
        cli = CommandLineInterface("test")
        cli.parser = m_parser
        cli.add_argument(
            "--yesterday",
            action="store_true",
            help="Download forecast files for previous day's date.",
        )
        m_parser.add_argument.assert_called_once_with(
            "--yesterday",
            action="store_true",
            help="Download forecast files for previous day's date.",
        )


class TestAddDateOption:
    """Unit tests for nemo_nowcast.cli.CommandLineInterface.add_date_option
    method.
    """

    def test_option_name(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        cli.add_date_option("--test-date", arrow.get("2016-09-22"), "help")
        assert cli.parser._actions[2].option_strings == ["--test-date"]

    def test_type(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        cli.add_date_option("--test-date", arrow.get("2016-09-22"), "help")
        assert cli.parser._actions[2].type == cli.arrow_date

    def test_default(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        cli.add_date_option("--test-date", arrow.get("2016-09-22"), "help")
        assert cli.parser._actions[2].default == arrow.get("2016-09-22")

    def test_help(self):
        cli = CommandLineInterface("test")
        cli.build_parser()
        cli.add_date_option("--test-date", arrow.get("2016-09-22"), "Help message.")
        expected = "Help message. Use YYYY-MM-DD format. Defaults to 2016-09-22."
        assert cli.parser._actions[2].help == expected


class TestArrowDate:
    """Unit tests for nemo_nowcast.cli.CommandLineInterface.arrow_date method."""

    def test_arrow_date(self):
        cli = CommandLineInterface("test")
        arw = cli.arrow_date("2016-09-22")
        expected = arrow.get(datetime(2016, 9, 22, 0, 0, 0), "utc")
        assert arw == expected

    def test_arrow_date_parse_erroe(self):
        cli = CommandLineInterface("test")
        with pytest.raises(argparse.ArgumentTypeError):
            cli.arrow_date("205-7-261")
