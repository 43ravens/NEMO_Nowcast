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

import yaml


def basic_arg_parser(module_name, description=None, add_help=True):
    """Return a command-line argument parser w/ handling for always-used args.

    The returned parser provides help messages, and handles the
    :option:`config_file` argument.

    :arg str module_name: Name of the module that the parser is for;
                          used to build the usage message.
                          Use dotted notation for modules below the
                          :kbd:`nowcast` namespace;
                          e.g. :kbd:`workers.download_weather`.

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
    parser.prog = 'python -m nemo_nowcast.{}'.format(module_name)
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
    return config


def deserialize_message(message):
    """Transform received message from str to message data structure.

    :arg str message: Message dict serialized using YAML.

    :returns:
    :rtype: :py:class:`collections.namedtuple`
    """
    msg = yaml.safe_load(message)
    message = namedtuple('Message', 'source, type, payload')
    return message(
        source=msg['source'],
        type=msg['type'],
        payload=msg['payload'],
    )
