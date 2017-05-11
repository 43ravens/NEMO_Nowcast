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

"""NEMO_Nowcast framework rotate_logs worker.

Iterate through the nowcast system logging handlers, calling the
:py:meth:`doRollover` method on any that are instances of
:py:class:`logging.handlers.RotatingFileHandler`.

This worker is normally launched in automation at the end of a nowcast
processing cycle (e.g. end of the day).

It can also be launched from the command-line by the nowcast administrator
as necessary for system maintenance.
"""
import logging
import logging.config
from pathlib import Path

from nemo_nowcast import NowcastWorker
from nemo_nowcast.fileutils import FilePerms


NAME = 'rotate_logs'
logger = logging.getLogger(NAME)


def main():
    """Set up and run the worker.

    For command-line usage see:

    :command:`python -m nemo_nowcast.workers.rotate_logs --help`
    """
    worker = NowcastWorker(
        NAME, description=__doc__, package='nemo_nowcast.workers')
    worker.init_cli()
    worker.run(rotate_logs, success, failure)


def success(parsed_args):
    # logger_name is required because file system handlers get loaded in
    # rotate_logs()
    logger.info('log files rotated', extra={'logger_name': NAME})
    msg_type = 'success'
    return msg_type


def failure(parsed_args):
    # logger_name is required because file system handlers get loaded in
    # rotate_logs()
    logger.critical('failed to rotate log files', extra={'logger_name': NAME})
    msg_type = 'failure'
    return msg_type


def rotate_logs(parsed_args, config, *args):
    # logger_name is required because file system handlers get loaded below
    logger.info('rotating log files', extra={'logger_name': NAME})
    checklist = []
    checklist_logger = logging.getLogger('checklist')
    if 'aggregator' in config['logging']:
        pub_handlers = config['logging']['publisher']['handlers']
        if 'checklist' in pub_handlers:
            pub_loggers = config['logging']['publisher']['loggers']
            config['logging']['aggregator']['handlers']['checklist'] = (
                pub_handlers['checklist'])
            try:
                config['logging']['aggregator']['loggers'].update(
                    {'checklist': pub_handlers['loggers']['checklist']})
            except KeyError:
                config['logging']['aggregator'].update(
                    {'loggers': {'checklist': pub_loggers['checklist']}})
        logging.config.dictConfig(config['logging']['aggregator'])
    for handler in logger.root.handlers + checklist_logger.handlers:
        if not hasattr(handler, 'when'):
            try:
                handler.flush()
                handler.doRollover()
            except AttributeError:
                # Handler without a doRollover() method;
                # Probably a StreamHandler
                continue
            logger.info(
                'log file rotated: {.baseFilename}'.format(handler),
                extra={'logger_name': NAME})
            p = Path(handler.baseFilename)
            p.chmod(FilePerms(user='rw', group='rw', other='r'))
            logger.debug(
                'new {.baseFilename} log file permissions set to rw-rw-r--'
                .format(handler), extra={'logger_name': NAME})
            checklist.append(handler.baseFilename)
    return checklist


if __name__ == '__main__':
    main()  # pragma: no cover
