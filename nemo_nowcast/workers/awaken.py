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

"""NEMO_Nowcast framework awaken worker example.

An example implementation of a worker module that does nothing other than send
messages to the manager.
This worker is intended to demonstrate how a worker is launched after the
sleep example worker finishes successfully.
"""
import logging

from nemo_nowcast import NowcastWorker


NAME = "awaken"
logger = logging.getLogger(NAME)


def main():
    """Set up and run the worker.

    For command-line usage see:

    :command:`python -m nemo_nowcast.workers.awaken --help`
    """
    worker = NowcastWorker(NAME, description=__doc__, package="nemo_nowcast.workers")
    worker.init_cli()
    worker.run(awaken, success, failure)


def success(parsed_args):
    logger.info("awoke")
    msg_type = "success"
    return msg_type


def failure(parsed_args):
    logger.critical("failed to awaken")
    msg_type = "failure"
    return msg_type


def awaken(parsed_args, config, *args):
    checklist = {"awoke": True}
    return checklist


if __name__ == "__main__":
    main()  # pragma: no cover
