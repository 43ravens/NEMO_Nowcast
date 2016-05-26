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

"""NEMO_Nowcast ZeroMQ message broker.
This broker provides the static point in the nowcast messaging framework,
allowing the nowcast_mgr to be restarted more or less at will.
"""
import logging
import logging.config
import os

from nemo_nowcast import lib

NAME = 'nowcast_broker'

logger = logging.getLogger(NAME)


def main():
    config = lib.load_config('docs/example_nowcast.yaml')
    logging.config.dictConfig(config['logging'])
    logger.info('running in process {}'.format(os.getpid()))


if __name__ == '__main__':
    main()
