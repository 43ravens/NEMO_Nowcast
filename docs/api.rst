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


.. _NEMO_NowcastPackageAPI:

*******************************
:kbd:`NEMO_Nowcast` Package API
*******************************

.. _NEMO_NowcastConfig:

System Configuration
====================

.. automodule:: nemo_nowcast.config
    :members:


.. _NEMO_NowcastMessage:

Message
=======

.. automodule:: nemo_nowcast.message
    :members:


.. _NEMO_NowcastMessageBroker:

Message Broker
==============

.. automodule:: nemo_nowcast.message_broker
    :members: main


.. _NEMO_NowcastManager:

Manager
=======

.. automodule:: nemo_nowcast.manager
    :members: main, NowcastManager


.. _NEMO_NowcastWorkerClasses:

Classes, Exceptions and Functions for Building Workers
======================================================

.. automodule:: nemo_nowcast.worker
    :members:


.. _NEMO_NowcastCommandLineInterface:

Command-line Interface
======================

.. automodule:: nemo_nowcast.cli
    :members:


.. _NEMO_NowcastWorkerLaunchScheduler:

Worker Launch Scheduler
=======================

.. automodule:: nemo_nowcast.scheduler
    :members: main


.. _NEMO_NowcastLogAggregator:

Log Aggregator
==============

.. automodule:: nemo_nowcast.log_aggregator
    :members: main


.. _NEMO_NowcastBuiltinWorkers:

Built-in Workers
================

The framework provides a few worker modules for tasks that are generic enough that they are likely to be required in most nowcast systems.
Please see :ref:`BuiltinWorkers` for descriptions of these workers and their intended use.

.. automodule:: nemo_nowcast.workers.rotate_logs
    :members:

.. automodule:: nemo_nowcast.workers.clear_checklist
    :members:


.. _ExampleWorkers:

Example Workers
===============

.. automodule:: nemo_nowcast.workers.sleep
    :members:

.. automodule:: nemo_nowcast.workers.awaken
    :members:


.. _ExampleNextWorkersModule:

Example :py:mod:`next_workers` Module
=====================================

.. automodule:: nemo_nowcast.next_workers
    :members:
