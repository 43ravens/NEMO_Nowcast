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

"""NEMO_Nowcast framework sleep worker example.

An example implementation of a worker module that does nothing other than sleep
for a specified number of seconds.
"""
import logging
import time

from nemo_nowcast import NowcastWorker


NAME = 'sleep'
logger = logging.getLogger(NAME)


def main():
    """Set up and run the worker.

    For command-line usage see:

    :command:`python -m nemo_nowcast.workers.sleep`
    """
    worker = NowcastWorker(
        NAME, description=__doc__, package='nemo_nowcast.workers')
    worker.init_cli()
    arg_defaults = {'sleep_time': 5}
    worker.arg_parser.set_defaults(**arg_defaults)
    worker.arg_parser.add_argument(
        '--sleep-time', type=int,
        help=(
            'number of seconds to sleep for; defaults to {[sleep_time]}'
            .format(arg_defaults))
    )
    worker.run(sleep, success, failure)


def success(parsed_args):
    logger.info(
        'slept for {.sleep_time} seconds'
        .format(parsed_args), extra={'sleep_time': parsed_args.sleep_time})
    msg_type = 'success'
    return msg_type


def failure(parsed_args):
    logger.critical(
        'failed to sleep for {.sleep_time} seconds'
        .format(parsed_args), extra={'sleep_time': parsed_args.sleep_time})
    msg_type = 'failure'
    return msg_type


def sleep(parsed_args, config, *args):
    time.sleep(parsed_args.sleep_time)
    checklist = {'sleep time': parsed_args.sleep_time}
    return checklist


if __name__ == '__main__':
    main()  # pragma: no cover
