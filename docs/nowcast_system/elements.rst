.. Copyright 2016-2020 Doug Latornell, 43ravens

.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at

..    http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _ElementsOfANowcastSystem:

****************************
Elements of a Nowcast System
****************************

**TODO**:

* Python package; e.g. `GoMSS_Nowcast`_

  .. _GoMSS_Nowcast: https://bitbucket.org/gomss-nowcast/gomss_nowcast

* version control is highly recommended
* nowcast system configuration
* workers
* next_workers module
* process management with supervisor
* distribute releases via an anaconda.org channel or conda-forge


.. _Logging:

Logging
=======

**TODO**:

* logging levels and readability of log files
* log file rotation and growth limitation
* environment variable substitution in logging config
* serve log files on web page if possible, or use log aggregation service
* exception logging to Sentry
* machine readable logging; JSON via Driftwood


.. _NextWorkersModule:

Next Workers Module
===================

**TODO**


.. _HandlingWorkerRaceConditions:

Handling Worker Race Conditions
-------------------------------

Occasionally when a collection of workers are launched to run concurrently by returning a list of :py:class:`nemo_nowcast.worker.NextWorker` instances from a :py:func:`next_workers.after_*` function a race condition is created among two or more of the workers.
When that happens it is impossible to know when of the racing workers :py:func:`~next_workers.after_*` functions to have return :py:class:`~nemo_nowcast.worker.NextWorker` instance(s) for the next step of the automation.

A concrete example of that situation is in the `Salish Sea Nowcast system`_ where :py:func:`nowcast.next_workers.after_collect_weather` includes the :ref:`salishseanowcast:GribToNetcdfWorker` and :ref:`salishseanowcast:DownloadLiveOceanWorker` workers in the list of next workers that it returns.
That results in a race conditions between the :ref:`salishseanowcast:GribToNetcdfWorker` and :ref:`salishseanowcast:MakeLiveOceanFilesWorker` workers that can allow the :ref:`salishseanowcast:UploadForcingWorker` workers to run before the :ref:`salishseanowcast:GribToNetcdfWorker` worker finishes,
causing the atmospheric forcing files to be incomplete for some of the NEMO runs.

.. _Salish Sea Nowcast system: https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#process-flow

To mitigate that situation we can return a 2-tuple from :py:func:`~nowcast.next_workers.after_collect_weather`.
The first element of the tuple is the ususal list of :py:class:`~nemo_nowcast.workers.NextWorker` instances.
The second element is a :py:class:`set` of worker names involved in the race condition,
for example:

.. code-block:: python

    next_workers =
        [
            NextWorker("nowcast.workers.get_NeahBay_ssh", args=["nowcast"]),
            NextWorker("nowcast.workers.grib_to_netcdf", args=["nowcast+"]),
            NextWorker("nowcast.workers.download_live_ocean"),
        ]
    )
    race_condition_workers = {"grib_to_netcdf", "make_live_ocean_files"}
    return next_workers, race_condition_workers

When the :ref:`NEMO_NowcastManager` sees a set of race condition workers returned from an :py:func:`~next_workers.after_*` function it sets up a data structure to manage the race condition.
As each of the workers in the race condition set finishes the :py:class:`~nemo_nowcast.worker.NextWorker` instance(s) they return are accumulated in a list instead of being launched immediately.
Once all of the race condition workers have finished the accumulated list of :py:class:`~nemo_nowcast.worker.NextWorker` instances is launched.
:py:func:`~logging.debug` level logging messages that describe the progress of the race conditions management are emitted.

.. note::
    At present only one race condition can be managed at a time.
