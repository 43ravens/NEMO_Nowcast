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
import logging
import os
import re
import socket
import time

import arrow
import requests
import yaml

from nemo_nowcast.worker import WorkerError


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


def get_web_data(
    file_url, filepath, logger_name,
    session=None,
    wait_exponential_multiplier=2,
    wait_exponential_max=60 * 60,
):
    """Download content from file_url and storeit in filepath.

    If the first download attempt fails, retry at exponentially increasing
    intervals until wait_exponential_max is exceeded.
    The first retry occurs after wait_exponential_multiplier seconds
    The delay until the next retry is calculated by multiplying the previous
    delay by wait_exponential_multiplier.

    So, with the default argument values, the first retry will occur
    2 seconds after the download fails, and subsequent retries will
    occur at 4, 8, 16, 32, 64, ..., 2048 seconds after each failure.

    :param str file_url: URL to download content from.

    :param filepath: File path/name at which to store the downloaded content.
    :type filepath: :py:class:`pathlib.Path`

    :param str logger_name: Name of the :py:class:`logging.Logger` to emit
                            messages on.

    :param session: Session object to use for TCP connection pooling
                    to improve performance for multiple requests to the same
                    host.
                    Defaults to :py:obj:`None` for simplicity,
                    in which case a session is created within the function.
                    If the function is called within loop,
                    the recommended use pattern is to create the session
                    outside the loop as a context manager:

                    .. code-block:: python

                        with requests.Session() as session:
                            for thing in iterable:
                                nemo_nowcast.lib.get_web_data(
                                    file_url, filepath, logger_name, session)

    :type session: :py:class:`requests.Session`

    :param wait_exponential_multiplier: Multiplicative factor that increases
                                        the time interval between retries.
                                        Also the number of seconds to wait
                                        before the first retry.
    :type wait_exponential_multiplier: int or float

    :param wait_exponential_max: Maximum number of seconds for the final retry
                                 wait interval.
                                 The actual wait time is less than or equal to
                                 the limit so it may be significantly less than
                                 the limit;
                                 e.g. with the default argument values the
                                 final retry wait interval will be 2048
                                 seconds.
    :type wait_exponential_max: int or float

    :return: :py:class:`requests.Response` headers
    :rtype: dict

    :raises: :py:exc:`nemo_nowcast.workers.WorkerError`
    """
    logger = logging.getLogger(logger_name)
    if session is None:
        session = requests.Session()
    def _get_data():
        try:
            response = session.get(file_url, stream=True)
            response.raise_for_status()
            return _handle_response_content(response, filepath)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            socket.error,
        ) as e:
            logger.debug('received {msg} from {url}'.format(msg=e, url=file_url))
            raise e
    try:
        _get_data()
    except:
        wait_seconds = wait_exponential_multiplier
        retries = 0
        while wait_seconds < wait_exponential_max:
            logger.debug('waiting {} seconds until retry'.format(wait_seconds))
            time.sleep(wait_seconds)
            try:
                _get_data()
            except:
                wait_seconds *= wait_exponential_multiplier
                retries += 1
        logger.error(
            'giving up; download from {url} failed {fail_count} times'
            .format(url=file_url, fail_count=retries+1))
        raise WorkerError


def _handle_response_content(response, filepath):
    """Store response content stream at filepath.
    """
    with filepath.open('wb') as f:
        for block in response.iter_content():
            if not block:
                break
            f.write(block)
    return response.headers
