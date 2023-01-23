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
Please follow the instructions on the Miniconda3`_  page to download and install it.

.. _Conda: https://docs.conda.io/en/latest/
.. _Miniconda3: https://docs.conda.io/en/latest/miniconda.html
.. _Linux Miniconda Install: https://docs.conda.io/en/latest/install/quick.html

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

.. _YAML: https://pyyaml.org/wiki/PyYAMLDocumentation

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


:kbd:`supervisord` Process Manager Configuration File
=====================================================

It is recommended to run the various long-running nowcast system processes under a process manager.
Doing so ensures that the processes will be restarted if they crash,
and provides a centralized interface for monitoring and controlling the processes.
We'll use `Supervisor`_ which was installed when you created your :ref:`CondaEnvironment`.

.. _Supervisor: http://supervisord.org/

:kbd:`supervisord` uses its own configuration file,
written using `INI`_ syntax.
Create a file called :file:`supervisord.ini` in your :file:`toy-nowcast/` directory with the following contents:

.. _INI: https://en.wikipedia.org/wiki/INI_file

.. code-block:: ini

    # Example supervisord process manager configuration file
    # for a NEMO_Nowcast framework system

    # Supervisor daemon and its interfaces
    [supervisord]
    logfile = %(ENV_NOWCAST_LOGS)s/supervisor.log
    pidfile = %(ENV_NOWCAST_LOGS)s/supervisor.pid
    childlogdir = %(ENV_NOWCAST_LOGS)s

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [inet_http_server]
    # This value must match that used in [supervisorctl]serverurl below
    port = localhost:9001


    # Supervisor interactive shell tool
    [supervisorctl]
    # Host and port values here must match those used in [inet_http_server]port above
    serverurl = http://localhost:9001
    prompt = nowcast-supervisor


    # Long-running processes that supervisor manages
    # Priority values define process startup order
    [program:message_broker]
    command = %(ENV_NOWCAST_ENV)s/bin/python3 -m nemo_nowcast.message_broker %(ENV_NOWCAST_YAML)s
    priority = 0
    autorestart = true

    [program:manager]
    command = %(ENV_NOWCAST_ENV)s/bin/python3 -m nemo_nowcast.manager %(ENV_NOWCAST_YAML)s
    priority = 1
    autorestart = true


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

.. _NEMO_Nowcast repository: https://github.com/43ravens/NEMO_Nowcast


Running the Nowcast System
==========================

Our "toy" nowcast system is ready to run.
Start the process manager with the command:

.. code-block:: bash

    (toy-nowcast) toy-nowcast$ supervisord -c supervisord.ini

We have configured :command:`supervisord` to send its logging messages,
and those from the processes it is managing to files in the directory pointed to by the envvar:`NOWCAST_LOGS` environment variable.
That is :file:`$HOME/toy-nowcast/` if you followed the instructions in the :ref:`EnvironmentVariables` section above.
The :file:`supervisor.log` file tells us about what :command:`supervisord` is doing.
If you use :command:`less` or :command:`cat` to look at it,
you should see something like ::

  2020-05-15 12:12:54,544 INFO RPC interface 'supervisor' initialized
  2020-05-15 12:12:54,544 CRIT Server 'inet_http_server' running without any HTTP authentication checking
  2020-05-15 12:12:54,545 INFO daemonizing the supervisord process
  2020-05-15 12:12:54,545 INFO supervisord started with pid 15937
  2020-05-15 12:12:55,548 INFO spawned: 'message_broker' with pid 15974
  2020-05-15 12:12:55,550 INFO spawned: 'manager' with pid 15975
  2020-05-15 12:12:56,773 INFO success: message_broker entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
  2020-05-15 12:12:56,773 INFO success: manager entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)

This shows :command:`supervisord` itself starting up,
then it spawning processes for our nowcast system's :ref:`MessageBroker` and :ref:`SystemManager` processes,
and confirming that those processes are running.

The logging messages from the :ref:`MessageBroker` and :ref:`SystemManager` processes.
Those files have names like:

* :file:`message_broker-stdout---supervisor-1_p3jss7.log`
* :file:`manager-stdout---supervisor-5x6e5ryj.log`

The 8 characters between :kbd:`---supervisor` and :kbd:`.log` are randomly generated each time :command:`supervisord` is started.
At this point,
those files contain the startup messages from those processes::

  2020-05-15 12:12:55,769 INFO [message_broker] running in process 15974
  2020-05-15 12:12:55,769 INFO [message_broker] read config from /home/doug/toy-nowcast/nowcast.yaml
  2020-05-15 12:12:55,769 INFO [message_broker] writing logging messages to local file system
  2020-05-15 12:12:55,769 INFO [message_broker] worker socket bound to port 4344
  2020-05-15 12:12:55,769 INFO [message_broker] manager socket bound to port 4343

from the :py:mod:`message_broker`,
and::

  2020-05-15 12:12:55,770 INFO [manager] running in process 15975
  2020-05-15 12:12:55,770 INFO [manager] read config from /home/doug/toy-nowcast/nowcast.yaml
  2020-05-15 12:12:55,770 INFO [manager] writing logging messages to local file system
  2020-05-15 12:12:55,771 INFO [manager] next workers module loaded from next_workers
  2020-05-15 12:12:55,771 INFO [manager] connected to localhost port 4343
  2020-05-15 12:12:55,771 WARNING [manager] checklist load failed:
  Traceback (most recent call last):
    File "/home/doug/NEMO_Nowcast/nemo_nowcast/manager.py", line 253, in _load_checklist
      with open(checklist_file, "rt") as f:
  FileNotFoundError: [Errno 2] No such file or directory: '/home/doug/toy-nowcast/nowcast_checklist.yaml'
  2020-05-15 12:12:55,772 WARNING [manager] running with empty checklist
  2020-05-15 12:12:55,772 DEBUG [manager] listening...

from the :py:mod:`manager`.
The latter tries to initialize the state of the system by reading from the :file:`nowcast_checklist.yaml` file and warns use that it can't find that file;
not surprising since this it the first time the system has been launched.
Finally,
it tells us that it has gone into its default state of listening for messages from workers.

You can shut the system down with the command

.. code-block:: bash

    (toy-nowcast)$ supervisorctl -c supervisord.ini shutdown

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

    (toy-nowcast)$ python3 -m nemo_nowcast.workers.sleep $NOWCAST_YAML

You should see logging messages that look like::

  2020-05-15 15:21:24,532 INFO [sleep] running in process 10011
  2020-05-15 15:21:24,532 INFO [sleep] read config from /home/doug/toy-nowcast/nowcast.yaml
  2020-05-15 15:21:24,532 INFO [sleep] writing log messages to local file system
  2020-05-15 15:21:24,532 INFO [sleep] connected to localhost port 4344
  2020-05-15 15:21:29,538 INFO [sleep] slept for 5 seconds
  2020-05-15 15:21:29,539 DEBUG [sleep] sent message: (success) sleep worker slept well
  2020-05-15 15:21:29,547 DEBUG [sleep] received message from manager: (ack) message acknowledged
  2020-05-15 15:21:29,547 DEBUG [sleep] shutting down

with a 5 second long pause in the middle.

If you look at the :kbd:`manager` log file again you should see additional logging messages that look like::

  2020-05-15 15:21:29,541 DEBUG [manager] received message from sleep: (success) sleep worker slept well
  2020-05-15 15:21:29,542 INFO [manager] checklist updated with [sleepyhead] items from sleep worker
  2020-05-15 15:21:29,550 DEBUG [manager] listening...

You can use :command:`tail`
(perhaps with its :kbd:`-f` option)
to see the end of the log files,
or you can use :command:`supervisorctl` for find and show you the tail of the log file for any of the processes it is managing:

.. code-block:: bash

    (toy-nowcast)$ supervisorctl -c supervisord.ini tail manager


**TODO**:

* exercises:

  * experiment with running sleep worker with :kbd:`--sleep-time` and/or :kbd:`--debug`
    command-line flags
  * run :command:`circusctl` in a 3rd terminal session
  * :command:`status`
  * add :py:func:`after_rotate_logs` function to :py:mod:`next_workers` module
  * run :command:`python -m nemo_nowcast.workers.rotate_logs nowcast.yaml`
  * add rotate_logs worker to after_awaken function,
    run sleep worker again
