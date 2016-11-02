.. Copyright 2016 Doug Latornell, 43ravens

.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at

..    http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _NowcastConfigFile:

**************************
Nowcast Configuration File
**************************

**TODO**


.. _LoggingConfig:

Logging Configuration
=====================

**TODO**

.. code-block:: yaml

    # Logging system configuration
    logging:
      version: 1
      disable_existing_loggers: False
      formatters:
        simple:
          format: '%(asctime)s %(levelname)s [%(name)s] %(message)s'
      handlers:
        console:
          class: logging.StreamHandler
          level: DEBUG
          formatter: simple
          stream: ext://sys.stdout
      root:
        level: DEBUG
        handlers:
         - console


.. _RotatingLogFilesAndLongRunningProcesses:

Rotating Log Files and Long-running Processes
---------------------------------------------

All logging handlers that are configured to use :py:class:`logging.handlers.RotatingFileHandler` receive special processing during the logging setup in the long-running :py:mod:`~nemo_nowcast.manager`,
:py:mod:`~nemo_nowcast.message_broker`,
and :py:mod:`~nemo_nowcast.scheduler` processes.
In those processes,
the :py:class:`logging.handlers.RotatingFileHandler` is replaced by a :py:class:`logging.handlers.WatchedFileHandler`.
That enables those processes to detect when the :py:mod:`nemo_nowcast.workers.rotate_logs` worker rotates the log files so that they start writing to the new log files.


.. _ZeroMQServerAndPortsConfig:

ZeroMQ Server and Ports
=======================

**TODO**

.. code-block:: yaml

    # Message system
    zmq:
      server: localhost
      ports:
        # traffic between manager and message broker
        manager: 4343
        # traffic between workers and message broker
        workers: 4344


.. _MessageRegistryConfig:

Message Registry
================

**TODO**

.. code-block:: yaml

    message registry:
      # Message types that the manager process can send and their meanings
      # Don't change this section without making corresponding changes in
      # the nemo_nowcast.manager module of the NEMO_Nowcast package.
      manager:
        ack: message acknowledged
        unregistered worker: ERROR - message received from unregistered worker
        unregistered message type: ERROR - unregistered message type received from worker
        no after_worker function: ERROR - after_worker function not found in next_workers module

      # Module from which to load :py:func:`after_<worker_name>` functions
      # that provide lists of workers to launch when :kbd:`worker_name` finishes
      next workers module: nowcast.next_workers

      workers:
        # Worker module name
        sleep:
          # The key in the system checklist that the manager maintains that is to
          # be used to hold message payload information provided by the
          # :kbd:`example` worker
          checklist key: sleepyhead
          # Message types that the :kbd:`example` worker can send and their meanings
          success: sleep worker slept well
          failure: sleep worker slept badly
          crash: sleep worker crashed
        awaken:
          checklist key: sleepyhead
          success: awaken worker awoke - where's the coffee?
          failure: awaken worker failed to awake
          crash: awaken worker crashed

Most messages are handled by the :ref:`SystemManager` by passing them to the :py:func:`after_worker_name` function in the :py:mod:`next_workers` module given by the :kbd:`next workers module` key.
For example,
when the manager receives a message with the type :kbd:`success` from the :py:mod:`~nemo_nowcast.workers.sleep` worker it calls the :py:func:`nowcast.next_workers.after_sleep` function with the message.


.. _SpecialMessageTypes:

Special Message Types
---------------------

There are several special message types that are handled differently by the manager:

* The  :kbd:`clear checklist` message that is sent by the :py:mod:`nemo_nowcast.workers.clear_checklist` worker causes the system state checklist to be written to a log file,
  then clears it.
  The :py:mod:`~nemo_nowcast.workers.clear_checklist` worker is typically run once per nowcast cycle (e.g. daily) at the end of processing,
  just before rotating the log files via the
  :py:mod:`nemo_nowcast.workers.rotate_logs` worker.
  The log file that the checklist is written to is given by the :kbd:`handlers.checklist.filename` key in the :ref:`LoggingConfig` section of the config file.
  The checklist is written as a pretty-printed representation of a Python dictionary.

* A :kbd:`need` message is expected to have a system state checklist key as its payload.
  The manager handles :kbd:`need` messages by returning an :kbd:`ack` message with the requested section of the checklist as its payload.

* A :kbd:`log.<level>` message is handles by the manager by emitting the message payload as a :kbd:`<level>` log message.
  So,
  a :kbd:`log.info` message from the :py:mod:`~nemo_nowcast.workers.sleep` worker with the payload :kbd:`I'm asleep!` would add a message like::

    2016-10-19 11:16:15,099 INFO [sleep] I'm asleep!

  to the log files.
  :kbd:`<level>` must be a logging level name defined in the Python `logging`_ module.

  .. _logging: https://docs.python.org/3/library/logging.html#levels


.. _ScheduledWorkersConfig:

Scheduled Workers
=================

The :kbd:`scheduled workers` section is an optional configuration section that is used to specify a list of workers that the :ref:`Scheduler` should launch,
when to launch them,
and what command-line options (if any) to use for the launches.
The period between system clock checks that the scheduler uses is hard-coded to 60 seconds.

.. note::
    Scheduled launching of workers is intended for use only in special cases in which a worker's launch time depends on factors outside of the nowcast system
    (such as the availability of atmospheric forcing model product files).

    The first choice for launching workers should be by the manager process in response to system state events
    (via the :ref:`NextWorkersModule`).

Example :kbd:`scheduled workers` configuration section:

.. code-block:: yaml

    # Workers scheduled to run at specific times
    scheduled workers:
        # Worker module name (fully qualified, dotted notation)
      - nowcast.workers.download_weather:
          # Time period for worker launch repetition
          every: day
          # Time at which to launch the worker
          # (quotes are required to ensure that time is interpreted as a string)
          at: '05:15'
          # Optional command-line options for the worker
          # (quotes are necessary to force interpretation as a string)
          cmd line opts: '12'


.. _ExampleNowcastConfigFile:

Example Nowcast Configuration File
==================================

Here is the complete example nowcast configuration YAML file that is discussed in the sections above:

.. literalinclude:: example_nowcast.yaml
    :language: yaml
