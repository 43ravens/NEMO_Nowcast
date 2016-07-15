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

"""Example :py:mod:`next_workers` module.

This should be implemented as :py:mod:`nowcast.next_workers` in a nowcast
system package the is built on top of the :kbd:`NEMO_Nowcast` package.
Please see the documentation at
http://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/index.html.

Functions to calculate lists of workers to launch after previous workers
end their work.

Function names **must** be of the form :py:func:`after_worker_name`.
"""
from nemo_nowcast.worker import NextWorker


def after_sleep(msg):
    """Calculate the list of workers to launch after the sleep example worker
    ends.

    :arg msg: Nowcast system message.
    :type msg: :py:func:`collections.namedtuple`

    :returns: Sequence of :py:class:`nemo_nowcast.worker.NextWorker` instances
              for worker(s) to launch next.
    :rtype: list
    """
    next_workers = {
        'crash': [],
        'failure': [],
        'success': [NextWorker('nemo_nowcast.workers.awaken')],
    }
    return next_workers[msg.type]


def after_awaken(msg):
    """Calculate the list of workers to launch after the awaken example worker
    ends.

    :arg msg: Nowcast system message.
    :type msg: :py:func:`collections.namedtuple`

    :returns: Sequence of :py:class:`nemo_nowcast.worker.NextWorker` instances
              for worker(s) to launch next.
    """
    next_workers = {
        'crash': [],
        'failure': [],
        'success': [],
    }
    return next_workers[msg.type]
