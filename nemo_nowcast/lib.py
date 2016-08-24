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
from collections import namedtuple
import os
import re

import arrow
import yaml


def base_arg_parser(
    module_name, package='nowcast', description=None, add_help=True,
):
    """Return a command-line argument parser w/ handling for always-used args.

    The returned parser provides help messages, and handles the
    :option:`config_file` argument.

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


def load_config(config_file):
    """Load the YAML config_file and return its contents as a dict.

    The value of config_file is added to the config dict with the key
    :kbd:`config_file`.

    :arg str config_file: Path/name of YAML configuration file for
                          the NEMO nowcast system.

    :returns: config dict
    """
    with open(config_file, 'rt') as f:
        config = yaml.safe_load(f)
    config['config_file'] = config_file
    envvar_pattern = re.compile(r'\$\(NOWCAST\.ENV\.(\w*)\)\w*')
    envvar_sub_keys = ('checklist file', 'python')
    for key in envvar_sub_keys:
        config[key] = envvar_pattern.sub(_replace_env, config[key])
    handlers = config['logging']['handlers']
    for handler in handlers:
        try:
            handlers[handler]['filename'] = envvar_pattern.sub(
                _replace_env, handlers[handler]['filename'])
        except KeyError:
            # Not a file handler
            pass
    return config


def _replace_env(var):
    try:
        return os.environ[var.group(1)]
    except KeyError:
        raise KeyError('environment variable not set: {}'.format(var.group(1)))


def deserialize_message(message):
    """Transform received message from str to message data structure.

    :arg str message: Message dict serialized using YAML.

    :returns: Named-tuple with attributes:

              * :py:attr:`source`: the name of the message source
              * :py:attr:`type`: the message type
              * :py:attr:`payload`: the message payload

    :rtype: :py:func:`collections.namedtuple`
    """
    msg = yaml.safe_load(message)
    message = namedtuple('Message', 'source, type, payload')
    return message(
        source=msg['source'],
        type=msg['type'],
        payload=msg['payload'],
    )


def serialize_message(source, msg_type, payload=None):
    """Construct a message data structure and transofrm it into a string
    suitable for sending.

    :arg str source: Name of the worker or manager sending the message.

    :arg str msg_type: Key of a message type that is defined for source
                       in the message registry section of the configuration
                       data structure.

    :arg payload: Content of message;
                  must be serializable by YAML such that it can be
                  deserialized by :func:`yaml.safe_load`.
    :type payload: Python object

    :returns: Message data structure serialized using YAML.
    """
    message = {'source': source, 'type': msg_type, 'payload': payload}
    return yaml.dump(message)


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
