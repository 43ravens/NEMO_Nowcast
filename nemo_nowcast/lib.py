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

"""NEMO_Nowcast framework library functions.
"""
import argparse

import arrow


def base_arg_parser(
    module_name, package='nowcast', description=None, add_help=True,
):
    """Return a command-line argument parser w/ handling for always-used args.

    The returned parser provides help messages, and handles the
    :kbd:`config_file` argument.

    :arg str module_name: Name of the module that the parser is for;
                          used to build the usage message.

    :arg str package: Name of the package that the module is part of;
                      used to build the usage message.
                      Use dotted notation;
                      e.g. :kbd:`nowcast.workers`.

    :arg str description: Brief description of what the module does that
                          will be displayed in help messages.

    :arg boolean add_help: Add a `-h/--help` option to the parser.
                           Disable this if you are going to use the returned
                           parser as a parent parser to facilitate adding more
                           args/options.

    :returns: :class:`argparse.ArgumentParser` object
    """
    parser = argparse.ArgumentParser(
        description=description, add_help=add_help)
    parser.prog = 'python -m {}.{}'.format(package, module_name)
    parser.add_argument(
        'config_file',
        help='Path/name of YAML configuration file for NEMO nowcast.'
    )
    return parser


def arrow_date(string, tz='Canada/Pacific'):
    """Convert a YYYY-MM-DD string to a timezone-aware arrow object
    or raise :py:exc:`argparse.ArgumentTypeError`.

    The time part of the resulting arrow object is set to 00:00:00.

    :arg string: YYYY-MM-DD string to convert.
    :type string: str

    :arg tz: Timezone of the date.
    :type tz: str

    :returns: Date string converted to an :py:class:`arrow.Arrow` object
              with tz as its timezone.

    :raises: :py:exc:`argparse.ArgumentTypeError`
    """
    try:
        arw = arrow.get(string, 'YYYY-MM-DD')
        return arrow.get(arw.date(), tz)
    except arrow.parser.ParserError:
        msg = (
            'unrecognized date format: {} - '
            'please use YYYY-MM-DD'.format(string))
        raise argparse.ArgumentTypeError(msg)
