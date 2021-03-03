.. Copyright 2016-2021 Doug Latornell, 43ravens

.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at

..    http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _LogAggregator:

**************
Log Aggregator
**************

The :ref:`NEMO_NowcastLogAggregator` is a long-running process that
collects log messages from all of the other nowcast system processes
(both workers,
and long-running processes like the manager)
and writes them to disk files,
etc. as configured in the :ref:`LoggingConfig`.

The log aggregator is intended for use in nowcast systems that have workers running on different hosts than the manager.
For example,
all of the pre- and post-processing runs on one machine but the NEMO runs are executed on a different computer server or cloud platform.
When the log aggregator process is used all of the other processes publish their log messages to network sockets.
The log aggregator subscribes to those sockets and processes the log messages as they are received.

The logging configuration for a nowcast system that uses the log aggregator is described under :ref:`DistributedLogging` in the :ref:`NowcastConfigFile` section.

The recommended way to launch the log aggregator is to put it under the control of a process manager like `Supervisor`_.
Please see :ref:`NowcastProcessMgmt` for details.

.. _Supervisor: http://supervisord.org/

.. note::
  It is necessary to ensure that the appropriate firewall rules are in place to allow traffic to pass between the machines on which remote workers are running and the machine that hosts the log aggregator via the logging port(s).

  Since manager/worker communication,
  and distributed logging all use ZeroMQ ports,
  it is crucial to ensure that all port numbers used are unique.
