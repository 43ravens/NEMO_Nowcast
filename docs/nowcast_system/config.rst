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


.. _DistributedLogging:

Distributed Logging
-------------------

Distributed logging is intended for use in nowcast systems that have workers running on different hosts than the manager.
For example,
all of the pre- and post-processing workers run on one machine but the NEMO runs are executed on a different computer server or cloud platform.
In such a system,
all of the elements
(message broker,
manager,
workers,
scheduler)
publish their log messages to network sockets.
The :ref:`NEMO_NowcastLogAggregator` process subscribes to those sockets and processes the log messages as they are received.

Here is an example logging configuration for distributed logging:

.. code-block:: yaml

    # Distributed logging system configuration
    logging:
      aggregator:
        version: 1
        disable_existing_loggers: False
        formatters:
          simple:
            format: '%(asctime)s %(levelname)s [%(logger_name)s] %(message)s'
        handlers:
          info_text:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: simple
            filename: $(NOWCAST.ENV.NOWCAST_LOGS)/nowcast.log
            backupCount: 7
          debug_text:
            class: logging.handlers.RotatingFileHandler
            level: DEBUG
            formatter: simple
            filename: $(NOWCAST.ENV.NOWCAST_LOGS)/nowcast.debug.log
            backupCount: 7
        root:
          level: DEBUG
          handlers:
           - info_text
           - debug_text

      publisher:
        version: 1
        disable_existing_loggers: False
        formatters:
          simple:
            format: '%(asctime)s %(levelname)s [%(name)s] %(message)s'
        handlers:
          console:
            class: logging.StreamHandler
            # Level 100 disables console logging.
            # Use worker --debug flag to enable console logging.
            level: 100
            formatter: simple
            stream: ext://sys.stdout
          zmq_pub:
            class: zmq.log.handlers.PUBHandler
            level: DEBUG
            formatter: simple
        root:
          level: DEBUG
          handlers:
           - console
           - zmq_pub

The :kbd:`aggregator` section provides the logging configuration that is used by the :ref:`NEMO_NowcastLogAggregator`,
typically to write log files on disk.
The :kbd:`publisher` section provides the logging configuration that is used by all the of the other elements of the nowcast system.
Those elements publish log messages on network ports defined in the :kbd:`zmq` section of the config file
(see below).
The log aggregator subscribes to all of those ports.
The :kbd:`aggregator` and :kbd:`publisher` sections are structured so that they can be read as Python :py:class:`dict` objects that obey the `Configuration dictionary schema`_ defined in the Python :py:mod:`logging` module.

.. _Configuration dictionary schema: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema

Important things to note in the :kbd:`aggregator` section:

* The use of :kbd:`%(logger_name)s` in the format string.
  This is done so that the name of the procees that published the log message will appear instead of :kbd:`log_aggregator` which is what happens if :kbd:`%(name)s` is used.

* The use of :py:class:`logging.handlers.RotatingFileHandler` logging handlers with :kbd:`backupCount` values set so that the log files don't grow without limit.
  Use the :ref:`RotateLogsWorker` to trigger rotation of the log files at an appropriate point in the daily automation cycle.

* The use of :kbd:`$(NOWCAST.ENV.NOWCAST_LOGS)` in the log :kbd:`filename` paths.
  Doing so allows the directory in which the log files are stored to be defined in the :envvar:`NOWCAST_LOGS` environment variable.
  That avoids having to hard code the log files directory path in multiple places in both the :ref:`NowcastConfigFile` and the :program:`supervisord` configuration file
  (see :ref:`NowcastProcessMgmt`)
  and risking the two getting out of sync.

In the :kbd:`publisher` section,
note that the logging handler used to publish log messages to the network sockets is :py:class:`zmq.log.handlers.PUBHandler`.

The network ports that the logging sockets are bound to are defined in the :kbd:`zmq` section of the config file:

.. code-block:: yaml

  # Message system
  zmq:
    host: localhost
    ports:
      # traffic between manager and message broker
      manager: 4343
      # traffic between workers and message broker
      workers: 4344
      # pub/sub logging traffic for log aggregator
      logging:
        message_broker: 4345
        manager: 4346
        scheduler: 4347
        workers: [4350, 4351, 4352]
        # **host:port pairs in lists must be quoted to project : characters**
        make_live_ocean_files: 'salish.eos.ubc.ca:4357'
        run_NEMO: ['salish.eos.ubc.ca:4354', '210.15.47.113:4354']
        watch_NEMO:
          - 'salish.eos.ubc.ca:4356'
          - '210.15.47.113:4356'

In this example the message broker,
manager,
scheduler,
and most workers run on the local host,
but the make_live_ocean_files worker runs on a remote host,
:kbd:`salish.eos.ubc.ca`,
and the run_NEMO and watch_NEMO workers run on 2 different remote hosts,
:kbd:`salish.eos.ubc.ca`,
and :kbd:`210.15.47.113`.
Note that the instances of the run_NEMO and watch_NEMO workers *must* use the same port numbers.

The :kbd:`run_NEMO` and :kbd:`watch_NEMO` keys show 2 different YAML syntaxes for lists.

Each process that publishes log messages must do so on a unique network port.
The value associated with the :kbd:`workers` key is a list of ports for workers running on the local host to use.
There should be enough ports in the list to ensure that all workers that run concurrently are able to find a port;
a :py:exc:`nemo_nowcast.worker.WorkerError` exception will be raised if all of the ports in the list are found to be in use when a worker starts up.

.. note::
  It is necessary to ensure that the appropriate firewall rules are in place to allow traffic to pass between the machines on which remote workers are running and the machine that hosts the log aggregator via the logging port(s).

  Since manager/worker communication,
  and distributed logging all use ZeroMQ ports,
  it is crucial to ensure that all port numbers used are unique.


.. _SystemStateChecklistLogging:

System State Checklist Logging
------------------------------

The system state checklist maintained by the :ref:`SystemManager` is written to disk as serialized YAML every time it is updated in a file given by the :kbd:`checklist file` configuration key.
By convention,
that file is :file:`$NOWCAST_LOGS/nowcast_checklist.yaml`.

It is also possible to add logging configuration to the system so that the checklist is logged to another file just before it is cleared by the :ref:`ClearChecklistWorker`.
Doing so preserves the checklist from previous days operations.
To enable checklist logging it is necessary to add a checklist logging handler to the logging configuration,
and to register a logger for the checklist.

For systems that use local filesystem logging,
that is accomplished by adding a :kbd:`checklist` section to the :kbd:`logging: handlers:` configuration section:

.. code-block:: yaml

    logging:
      ...
      handlers:
        ...
        checklist:
          class: logging.handlers.RotatingFileHandler
          level: INFO
          formatter: simple
          filename: $(NOWCAST.ENV.NOWCAST_LOGS)/checklist.log
          backupCount: 7

The checklist logger is registered by adding a :kbd:`logging: loggers: checklist:` section:

.. code-block:: yaml

    logging:
      ...
      loggers:
        checklist:
          qualname: checklist
          level: INFO
          propagate: False
          handlers:
            - checklist

These examples set up a :py:class:`~logging.handlers.RotatingFileHandler` for the checklist that writes it to the :file:`$NOWCAST_LOGS/checklist.log` file and retains the previous 7 versions of that file when the log files are rotated.

For systems that use :ref:`DistributedLogging`,
similar configuration sections are required,
but they are added to the :kbd:`logging: publisher:` configuration:

.. code-block:: yaml

    logging:
      ...
      publisher:
        ...
        handlers:
          ...
          checklist:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: simple
            filename: $(NOWCAST.ENV.NOWCAST_LOGS)/checklist.log
            backupCount: 7
        ...
        loggers:
          checklist:
            qualname: checklist
            level: INFO
            propagate: False
            handlers:
              - checklist


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
