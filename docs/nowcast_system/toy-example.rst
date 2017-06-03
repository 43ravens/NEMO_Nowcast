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


.. _ToyExample:

***********************************
A "Toy" Example of a Nowcast System
***********************************

In the spirit of "learn by doing",
this section presents the practical details of building and operating a nowcast system by setting up a "toy" nowcast system with a few trival :ref:`ExampleWorkers`.
The :ref:`subsequent sections <BuildingANowcastSystem>` provide more detailed reference documentation about building and operating software automation systems based on this framework.


.. _CondaEnvironment:

Conda Environment
=================

We'll use a `Conda`_ environment to isolate Python package installation.
`Miniconda3`_ provides the :command:`conda` package manager and environment management tools.
Please follow the `Linux Miniconda Install`_ instructions to download and install Miniconda.

.. _Conda: http://conda.pydata.org/docs/
.. _Miniconda3: http://conda.pydata.org/docs/install/quick.html
.. _Linux Miniconda Install: http://conda.pydata.org/docs/install/quick.html#linux-miniconda-install

Once that is done,
create a conda environment with the `NEMO_Nowcast`_ package and its dependencies installed in it with the command:

.. _NEMO_Nowcast: https://anaconda.org/GoMSS-Nowcast/nemo_nowcast

.. code-block:: bash

    $ conda create -n toy-nowcast -c gomss-nowcast nemo_nowcast

Activate the environment with:

.. code-block:: bash

    $ source activate toy-nowcast

To deactivate the environment later,
use:

.. code-block:: bash

    (toy-nowcast)$ source deactivate toy-nowcast


:file:`nowcast` Directory
=========================

Create a directory to hold the nowcast system files.
It can be anywhere,
but for simplicity we'll put it in your :envvar:`$HOME` directory:

.. code-block:: bash

    (toy-nowcast)$ mkdir $HOME/toy-nowcast


.. _EnvironmentVariables:

Environment Variables
=====================

The :kbd:`NEMO_Nowcast` package uses environment variables for some fundamental elements of the configuration of a nowcast system.
:envvar:`NOWCAST_ENV` must be set to the :ref:`CondaEnvironment` path.
An easy way to do that is:

.. code-block:: bash

    (toy-nowcast)$ export NOWCAST_ENV=$CONDA_PREFIX

:envvar:`NOWCAST_LOGS` must be set to a directory where the nowcast system log files will be stored.
For simplicity we'll just use our :file:`$HOME/toy-nowcast/` directory:

.. code-block:: bash

    (toy-nowcast)$ export NOWCAST_LOGS=$HOME/toy-nowcast/

:envvar:`NOWCAST_YAML` must be set to nowcast system configuration file,
which we will create in a moment:

.. code-block:: bash

    (toy-nowcast)$ export NOWCAST_YAML=$HOME/toy-nowcast/nowcast.yaml


Nowcast System Configuration File
=================================

The configuration of a nowcast system is defined in a :ref:`NowcastConfigFile`.
Configuration files are written in `YAML`_,
the basic element of which is key-value pairs.

.. _YAML: http://pyyaml.org/wiki/PyYAMLDocumentation

Create a file called :file:`nowcast.yaml` in your :file:`toy-nowcast/` directory with the following contents.
(you can omit the lines that start with :kbd:`#` if you wish,
they are comments):

.. code-block:: yaml

    # Example system configuration file for a NEMO_Nowcast framework system

    # System status checklist file
    checklist file: $(NOWCAST.ENV.NOWCAST_LOGS)/nowcast_checklist.yaml

    # Python interpreter in environment with all dependencies installed
    # Used to launch workers
    python: $(NOWCAST.ENV.NOWCAST_ENV)/bin/python

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

    # Message system
    zmq:
      host: localhost
      ports:
        # traffic between manager and message broker
        manager: 4343
        # traffic between workers and message broker
        workers: 4344

    message registry:
      # Message types that the manager process can send and their meanings
      # Don't change this section without making corresponding changes in
      # the nemo_nowcast.manager module of the NEMO_Nowcast package.
      manager:
        ack: message acknowledged
        checklist cleared: system checklist cleared
        unregistered worker: ERROR - message received from unregistered worker
        unregistered message type: ERROR - unregistered message type received from worker
        no after_worker function: ERROR - after_worker function not found in next_workers module

      # Module from which to load :py:func:`after_<worker_name>` functions
      # that provide lists of workers to launch when :kbd:`worker_name` finishes
      next workers module: next_workers

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

The contents of the configuration file are described in detail in the :ref:`NowcastConfigFile` section of these docs.


:kbd:`circus` Process Manager Configuration File
================================================

It is recommended to run the various long-running nowcast system processes under a process manager.
Doing so ensures that the processes will be restarted if they crash,
and provides a centralized interface for monitoring and controlling the processes.
We'll use `Circus`_ which was installed when you created your :ref:`CondaEnvironment`.

.. _Circus: https://circus.readthedocs.io/en/latest/

:kbd:`circus` uses its own configuration file,
written using `INI`_ syntax.
Create a file called :file:`circus.ini` in your :file:`toy-nowcast/` directory with the following contents:

.. _INI: https://en.wikipedia.org/wiki/INI_file

.. code-block:: ini

    # Example circus process manager configuration file
    # for a NEMO_Nowcast framework system

    [watcher:message_broker]
    copy_env = True
    cmd = $(CIRCUS.ENV.NOWCAST_ENV)/bin/python
    args = -m nemo_nowcast.message_broker $(CIRCUS.ENV.NOWCAST_YAML)
    singleton = True
    send_hup = True
    use_sockets = False

    [watcher:manager]
    copy_env = True
    cmd = $(CIRCUS.ENV.NOWCAST_ENV)/bin/python
    args = -m nemo_nowcast.manager $(CIRCUS.ENV.NOWCAST_YAML)
    singleton = True
    send_hup = True
    use_sockets = False

    [watcher:scheduler]
    copy_env = True
    cmd = $(CIRCUS.ENV.NOWCAST_ENV)/bin/python
    args = -m nemo_nowcast.scheduler $(CIRCUS.ENV.NOWCAST_YAML)
    singleton = True
    send_hup = True
    use_sockets = False


:py:mod:`next_workers` Module
=============================

Now we need to create the :py:mod:`next_workers` module for our system.
As described in the :ref:`SystemManager` section,
The :py:mod:`next_workers` module contains functions that return a sequence of :py:class:`nemo_nowcast.worker.NextWorker` objects that specify workers and their command-line arguments that the manager should launch when it receives a completion message from a worker.

We'll start with a minimal :py:mod:`next_workers` module.
Create a file called :file:`next_workers.py` in your :file:`toy-nowcast/` directory and put the following code in it:

.. code-block:: python

    """Example :py:mod:`next_workers` module.

    Functions to calculate lists of workers to launch after previous workers
    end their work.

    Function names **must** be of the form :py:func:`after_worker_name`.
    """
    from nemo_nowcast import NextWorker


    def after_sleep(msg, config, checklist):
        """Calculate the list of workers to launch after the sleep example worker
        ends.

        :arg msg: Nowcast system message.
        :type msg: :py:func:`collections.namedtuple`

        :arg config: :py:class:`dict`-like object that holds the nowcast system
                     configuration that is loaded from the system configuration
                     file.
        :type config: :py:class:`nemo_nowcast.config.Config`

        :arg dict checklist: System checklist: data structure containing the
                             present state of the nowcast system.

        :returns: Sequence of :py:class:`nemo_nowcast.worker.NextWorker` instances
                  for worker(s) to launch next.
        :rtype: list
        """
        next_workers = {
            'crash': [],
            'failure': [],
            'success': [],
        }
        return next_workers[msg.type]

This module provides an :py:func:`after_sleep` function that tells the manager what worker(s) to launch after the :py:mod:`sleep` worker finishes.
The :py:mod:`nemo_nowcast.workers.sleep` is example worker that is included in the `NEMO_Nowcast repository`_.
Note that our :py:func:`after_sleep` function always returns an empty list;
that is,
we're saying that the manager should not launch another worker.
Also note that the 3 keys in the :py:obj:`next_workers` dict correspond to the 3 message types registered for the :py:mod:`sleep` worker in our :file:`nowcast.yaml` file.

.. _NEMO_Nowcast repository: https://bitbucket.org/43ravens/nemo_nowcast


Running the Nowcast System
==========================

Our "toy" nowcast system is ready to run.
Start the process manager with the command:

.. code-block:: bash

    (toy-nowcast) toy-nowcast$ circusd circus.ini

and you should see output link::

  2017-05-25 16:46:36 circus[9160] [INFO] Starting master on pid 9160
  2017-05-25 16:46:36 circus[9160] [INFO] Arbiter now waiting for commands
  2017-05-25 16:46:36 circus[9160] [INFO] manager started
  2017-05-25 16:46:36 circus[9160] [INFO] message_broker started
  2017-05-25 16:46:36 circus[9160] [INFO] scheduler started
  2017-05-25 16:46:36,914 INFO [scheduler] running in process 9202
  2017-05-25 16:46:36,914 INFO [scheduler] read config from /media/doug/warehouse/43ravens/projects/gomss-nowcast/toy-nowcast/nowcast.yaml
  2017-05-25 16:46:36,914 INFO [scheduler] writing logging messages to local file system
  2017-05-25 16:46:36,933 INFO [message_broker] running in process 9201
  2017-05-25 16:46:36,933 INFO [message_broker] read config from /media/doug/warehouse/43ravens/projects/gomss-nowcast/toy-nowcast/nowcast.yaml
  2017-05-25 16:46:36,933 INFO [message_broker] writing logging messages to local file system
  2017-05-25 16:46:36,934 INFO [message_broker] worker socket bound to port 4344
  2017-05-25 16:46:36,934 INFO [message_broker] manager socket bound to port 4343
  2017-05-25 16:46:36,951 INFO [manager] running in process 9200
  2017-05-25 16:46:36,951 INFO [manager] read config from /media/doug/warehouse/43ravens/projects/gomss-nowcast/toy-nowcast/nowcast.yaml
  2017-05-25 16:46:36,951 INFO [manager] writing logging messages to local file system
  2017-05-25 16:46:36,952 INFO [manager] next workers module loaded from next_workers
  2017-05-25 16:46:36,952 INFO [manager] connected to localhost port 4343
  2017-05-25 16:46:36,952 WARNING [manager] checklist load failed:
  Traceback (most recent call last):
    File "/home/doug/warehouse/conda_envs/toy-nowcast/lib/python3.5/site-packages/nemo_nowcast/manager.py", line 244, in _load_checklist
      with open(checklist_file, 'rt') as f:
  FileNotFoundError: [Errno 2] No such file or directory: '/media/doug/warehouse/43ravens/projects/gomss-nowcast/toy-nowcast/nowcast_checklist.yaml'
  2017-05-25 16:46:36,953 WARNING [manager] running with empty checklist
  2017-05-25 16:46:36,953 DEBUG [manager] listening...

We have configured out toy system to send all of its logging messages to the screen so that we can easily see what is going on.
In a production system the logging messages would be configured to go to files and the circus manager would be run as a daemon so that the system would operate without being attached to a terminal session.

The first group of messages,
identified with :kbd:`circus[9160]`,
are from the process manager.
They tell us that it is running,
and that it has started our nowcast system's :ref:`SystemManager`,
:ref:`MessageBroker`,
and :ref:`Scheduler` processes.

Next come startup messages from each of those processes.
The :py:mod:`manager` tries to initialize the state of the system by reading from the :file:`nowcast_checklist.yaml` file and warns use that it can't find that file;
not surprising since this it the first time the system has been launched.

Finally,
the :py:mod:`manager` tells us that it has gone into its default state of listening for messages from workers.

You can shut the system down with a :kbd:`Ctrl-C` in this terminal session,
but leave it running so that we can play with the :py:mod:`sleep` worker.


Running the :py:mod:`sleep` Worker
==================================

Start another terminal session,
activate your :kbd:`toy-nowcast` :ref:`CondaEnvironment` in it,
and set up the :ref:`EnvironmentVariables`:

.. code-block:: bash

    $ cd toy-nowcast
    $ source activate toy-nowcast
    (toy-nowcast)$ export NOWCAST_ENV=$CONDA_PREFIX
    (toy-nowcast)$ export NOWCAST_LOGS=$HOME/toy-nowcast/
    (toy-nowcast)$ export NOWCAST_YAML=$HOME/toy-nowcast/nowcast.yaml

Now you can run the :py:mod:`sleep` worker with:

.. code-block:: bash

    (toy-nowcast)$ python -m nemo_nowcast.workers.sleep $NOWCAST_YAML

You should see logging messages that look like::

  2017-05-25 17:19:47,143 INFO [sleep] running in process 17464
  2017-05-25 17:19:47,143 INFO [sleep] read config from /media/doug/warehouse/43ravens/projects/gomss-nowcast/toy-nowcast/nowcast.yaml
  2017-05-25 17:19:47,143 INFO [sleep] writing log messages to local file system
  2017-05-25 17:19:47,144 INFO [sleep] connected to localhost port 4344
  2017-05-25 17:19:52,148 INFO [sleep] slept for 5 seconds
  2017-05-25 17:19:52,149 DEBUG [sleep] sent message: (success) sleep worker slept well
  2017-05-25 17:19:52,155 DEBUG [sleep] received message from manager: (ack) message acknowledged
  2017-05-25 17:19:52,155 DEBUG [sleep] shutting down

with a 5 second long pause in the middle.

In the 1st terminal session
(where you launched :program:`circusd`)
you should see logging messages that look like::




**TODO**:

* run :command:`python -m nemo_nowcast.workers.sleep nowcast.yaml` in a 2nd terminal session

* exercises:

  * experiment with running sleep worker with :kbd:`--sleep-time` and/or :kbd:`--debug`
    command-line flags
  * run :command:`circusctl` in a 3rd terminal session
  * :command:`status`
  * add :py:func:`after_rotate_logs` function to :py:mod:`next_workers` module
  * run :command:`python -m nemo_nowcast.workers.rotate_logs nowcast.yaml`
  * add rotate_logs worker to after_awaken function,
    run sleep worker again
