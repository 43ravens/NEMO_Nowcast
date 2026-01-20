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

"""NEMO_Nowcast framework command-line interface.

Provides a command-line interface argument parser for nowcast system components.
The parser includes handling for the always-required :kbd:`config_file`
argument.
"""

import argparse

import arrow
import attr


@attr.s
class CommandLineInterface:
    """Construct a :py:class:`nemo_nowcast.cli.CommandLineInterface` instance."""

    #: Name of the module that the parser is for;
    #: used to build the usage message.
    module_name = attr.ib()
    #: Name of the package that the module is part of;
    #: used to build the usage message.
    #: Use dotted notation; e.g. :kbd:`nowcast.workers`.
    package = attr.ib(default="nowcast")
    #: Brief description of what the module does that will be displayed in the
    #: help messages.
    description = attr.ib(default=None)
    #: Argument parser; created by calling the
    #: :py:meth:`~nemo_nowcast.cli.CommandLineInterface.build_parser` method.
    parser = attr.ib(default=None, init=False)

    def build_parser(self, add_help=True):
        """Return a command-line argument parser with its description and
        usage messages set, and :kbd:`config_file` as a required argument.

        :arg boolean add_help: Add a `-h/--help` option to the parser.
                               Disable this if you are going to use the
                               returned parser as a parent parser to facilitate
                               adding more args/options.

        :return: :class:`argparse.ArgumentParser` object
        """
        self.parser = argparse.ArgumentParser(
            description=self.description, add_help=add_help
        )
        self.parser.prog = f"python -m {self.package}.{self.module_name}"
        self.parser.add_argument(
            "config_file", help="Path/name of YAML configuration file for NEMO nowcast."
        )

    def add_argument(self, *args, **kwargs):
        """Add an argument to the CLI parser.

        This is a thin wrapper around
        :py:meth:`argparse.ArgumentParser.add_argument` that accepts
        that method's arguments.
        """
        self.parser.add_argument(*args, **kwargs)

    def add_date_option(self, name, default, help):
        """Add a date option to the CLI parser.

        The stored date is an :py:class:`arrow.Arrow` object.

        This is a thin wrapper around
        :py:meth:`argparse.ArgumentParser.add_argument` that sets the
        type of the option to
        :py:meth:`nemo_nowcast.cli.CommandLineInterface.arrow_date`,
        and append information about the option's format and default value
        to the *help* message.

        :arg str name: Option name/flag; e.g. :kbd:`--forecast-date`.

        :arg default: Date to use when the option is not included on the
                      command-line; typically :kbd:`arrow.now().floor('day')`.
        :type default: :py:class:`arrow.Arrow`

        :arg str help: Help message. The words
                       "Use YYYY-MM-DD format. Defaults to {default}."
                       are appended to the message provided,
                       where "{default}" is the value of *default*
                       formatted as :kbd:`YYYY-MM-DD`.
        """
        self.parser.add_argument(
            name,
            type=self.arrow_date,
            default=default,
            help=(
                f"{help} Use YYYY-MM-DD format. Defaults to {default.format('YYYY-MM-DD')}."
            ),
        )

    @staticmethod
    def arrow_date(string):
        """Convert a YYYY-MM-DD string to a UTC arrow object or raise
        :py:exc:`argparse.ArgumentTypeError`.

        The time part of the resulting arrow object is set to 00:00:00.

        :arg str string: YYYY-MM-DD string to convert.

        :returns: Date string converted to a UTC :py:class:`arrow.Arrow` object.

        :raises: :py:exc:`argparse.ArgumentTypeError`
        """
        try:
            return arrow.get(string, "YYYY-MM-DD")
        except arrow.parser.ParserError:
            msg = f"unrecognized date format: {string} - please use YYYY-MM-DD"
            raise argparse.ArgumentTypeError(msg)
