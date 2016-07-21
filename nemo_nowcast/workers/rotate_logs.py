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
"""
import logging

from nemo_nowcast.worker import NowcastWorker


NAME = 'rotate_logs'
logger = logging.getLogger(NAME)


def main():
    """Set up and run the worker.

    For command-line usage see:

    :command:`python -m nemo_nowcast.workers.rotate_logs`
    """
    worker = NowcastWorker(
        NAME, description=__doc__, package='nemo_nowcast.workers')
    worker.run(rotate_logs, success, failure)


def success(parsed_args):
    logger.info('log files rotated')
    msg_type = 'success'
    return msg_type


def failure(parsed_args):
    logger.critical('failed to rotate log files')
    msg_type = 'failure'
    return msg_type


def rotate_logs(parsed_args, config):
    logger.info('rotating log files')
    checklist = []
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if not hasattr(handler, 'when'):
            try:
                handler.doRollover()
            except AttributeError:
                # Handler without a doRollover() method;
                # Probably a StreamHandler
                continue
            logger.info('log file rotated: {.baseFilename}'.format(handler))
            checklist.append(handler.baseFilename)
    return checklist


if __name__ == '__main__':
    main()  # pragma: no cover
