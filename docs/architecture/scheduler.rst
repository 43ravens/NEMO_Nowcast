.. Copyright 2016 – present Doug Latornell, 43ravens

.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at

..    http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _Scheduler:

*********
Scheduler
*********

The :ref:`NEMO_NowcastWorkerLaunchScheduler` is a long-running process that periodically checks the system clock and launches workers when their scheduled time to run is reached.
It is intended for use only in special cases in which a worker's launch time depends on factors outside of the nowcast system
(such as the availability of atmospheric forcing model product files).

When the scheduler is started it uses the information in the :ref:`ScheduledWorkersConfig` section of the system configuration file to build the worker launch schedule.
After that,
the scheduler goes into an infinite loop in which it checks to see if it is time to launch a worker and then sleeps for a period of time.
The default sleep period is 60 seconds.

.. note::
    Scheduled launching of workers is intended for use only in special cases.

    The first choice for launching workers should be by the manager process in response to system state events
    (via the :ref:`NextWorkersModule`).

The recommended way to launch the scheduler is to put it under the control of a process manager like `Supervisor`_.
Please see :ref:`NowcastProcessMgmt` for details.

.. _Supervisor: https://supervisord.org/
