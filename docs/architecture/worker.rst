.. NEMO Nowcast Framework documentation master file

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


.. _Worker:

******
Worker
******

Workers are short-lived processes that are launched when the nowcast system state is such that it is time for them to do their job.
Their processes end when their job is completed and they have communicated their success or failure to the manager.

Workers are Python modules that can be executed from the command-line.
The manager launches workers in subprocesses in a way that is equivalent to launching them manually from the command-line.
That enables system failures to be overcome by running one or more workers manually in such a way that the nowcast system automation restarts.

The design intent of workers is inspired by the "do one thing and do it well" aspect of the Unix philosophy.
Having small,
independent workers facilitates restarting the nowcast system automation at (almost) any point in the daily processing in the event of problems.
To the extent possible,
workers should be `idempotent`_ so that they can be run multiple times if necessary to recover from problems.
Workers should use :ref:`Logging` to record significant events in the nowcast system log files to facilitate monitoring of the system,
and diagnosis and recovery from problems.
Workers often have command-line option flags that enable their execution to be customized;
for example a :kbd:`--run-date` flag might allow a worker to operate on run results from a specific date.

.. _idempotent: https://en.wikipedia.org/wiki/Idempotence

Small,
independent,
idempotent workers that have command-line option flags and that contribute well to the nowcast system log files are key to making a nowcast system flexible,
robust,
fault tolerant,
and easy to maintain.

The framework provides:

* The :py:mod:`nemo_nowcast.worker` module that contains classes for the construction and use of worker modules
* A collection of :ref:`BuiltinWorkers` that are likely to be of use in many nowcast systems built on the framework
* :ref:`ExampleWorkers`,
  an :ref:`ExampleNextWorkersModule`,
  and example configuration files
  (:ref:`ExampleNowcastConfigFile` and :ref:`ExampleCircusConfigFile`)
  sufficient to create a :ref:`ToyExample` that demonstrates how the workers,
  manager,
  and message broker processes interact

By default all workers based on :py:class:`nemo_nowcast.worker.NowcastWorker` accept the path and name of a :ref:`NowcastConfigFile` as a required command-line argument.
They also accept :kbd:`--help` or :kbd:`-h`,
and :kbd:`--debug` as command-line options.

Running a worker with the :kbd:`--help` or :kbd:`-h` flag provides information about the worker and how to run it::

  $ python -m nemo_nowcast.workers.rotate_logs nowcast.yaml -h
  usage: python -m nemo_nowcast.workers.rotate_logs [-h] [--debug] config_file

  NEMO_Nowcast framework rotate_logs worker. Iterate through the nowcast system
  logging handlers, calling the :py:meth:`doRollover` method on any that are
  instances of :py:class:`logging.handlers.RotatingFileHandler`.

  positional arguments:
    config_file  Path/name of YAML configuration file for NEMO nowcast.

  optional arguments:
    -h, --help   show this help message and exit
    --debug      Send logging output to the console instead of the log file. Log
                 messages that would normally be sent to the manager are sent to
                 the console, suppressing interactions with the manager such as
                 launching other workers. Intended only for use when the worker
                 is run in foreground from the command-line.

As the output above says,
the :kbd:`--debug` flag changes how the worker interacts with the nowcast messaging system and log files in such a way that the worker is disconnected from the system.
That is useful for testing,
debugging,
and sometimes for maintenance of the system or recovery from problems.

The :ref:`CreatingNowcastWorkers` section provides a detailed description of how to create a worker module.

The :ref:`ExampleWorkers` and the :ref:`BuiltinWorkers` provided for use in nowcast system deployments serve as examples of how to write your own worker modules.
