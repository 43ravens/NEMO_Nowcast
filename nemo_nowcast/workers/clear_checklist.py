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

"""NEMO_Nowcast framework clear_checklist worker.

Send a message to the nowcast system manager requesting that it clear its
system state checklist.

This worker is normally launched in automation at the end of a nowcast
processing cycle (e.g. end of the day), just prior to launching the
:py:mod:`nemo_nowcast.workers.rotate_logs` worker.

It can also be launched from the command-line by the nowcast administrator
as necessary for system maintenance.
"""
import logging

import nemo_nowcast.lib
from nemo_nowcast.worker import NowcastWorker


NAME = 'clear_checklist'
logger = logging.getLogger(NAME)


def main():
    """Set up and run the worker.

    For command-line usage see:

    :command:`python -m nemo_nowcast.workers.clear_checklist`
    """
    worker = NowcastWorker(
        NAME, description=__doc__, package='nemo_nowcast.workers')
    worker.init_cli()
    worker.run(clear_checklist, success, failure)


def success(parsed_args):
    logger.info('nowcast system checklist cleared')
    msg_type = 'success'
    return msg_type


def failure(parsed_args):
    logger.critical('failed to clear nowcast system checklist')
    msg_type = 'failure'
    return msg_type


def clear_checklist(parsed_args, config, tell_manager):
    logger.info('requesting that manager clear system state checklist')
    tell_manager('clear checklist')
    # Don't return a checklist entry because we just cleared it!


if __name__ == '__main__':
    main()  # pragma: no cover
