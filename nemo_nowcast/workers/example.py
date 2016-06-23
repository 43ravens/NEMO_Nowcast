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

"""NEMO_Nowcast framework worker example.

An example implementation of a worker module that does nothing other than sleep
for a specified number of seconds.
"""
from nemo_nowcast.worker import NowcastWorker


def main():
    """Set up and run the worker.

    For command-line usage see:

    :command:`python -m nemo_nowcast.workers.example`
    """
    worker = NowcastWorker(
        'example', description=__doc__, package='nemo_nowcast.workers')
    worker.run()


if __name__ == '__main__':
    main()  # pragma: no cover
