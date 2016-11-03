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


.. _CreatingNowcastWorkerModules:

*******************************
Creating Nowcast Worker Modules
*******************************

Nowcast workers are Python modules that can be imported from :py:mod:`nowcast.workers`.
They are composed of some standard code to enable them to interface with the nowcast system messaging and logging framework,
and one or more functions to execute their task in the nowcast system.
Most of the standard code is centred around setup of a :py:class:`~nemo_nowcast.worker.NowcastWorker` object and executing method calls on it.
The worker object is an instance of the :py:class:`nemo_nowcast.worker.NowcastWorker` class.


.. _SkeletonWorkerExample:

Skeleton Worker Example
=======================

Here is a skeleton example of a worker module showing the standard code.
It is explained,
line by line,
below.
Actual
(and obviously, more complicated)
worker modules can be found in:

* :ref:`BuiltinWorkers`
* :ref:`gomssnowcast:GoMSS_NowcastSystemWorkers`
* :ref:`salishseanowcast:SalishSeaNowcastSystemWorkers`

.. code-block:: python
    :linenos:

    """NEMO Nowcast worker to ...

    ...
    """
    import logging

    from nemo_nowcast import NowcastWorker


    NAME = 'worker_name'
    logger = logging.getLogger(NAME)


    def main():
        """Set up and run the worker.

        For command-line usage see:

        :command:`python -m nemo_nowcast.workers.worker_name --help`
        """
        worker = NowcastWorker(NAME, description=__doc__)
        worker.init_cli()
        worker.run(worker_func, success, failure)


    def success(parsed_args):
        logger.info('success message')
        msg_type = 'success'
        return msg_type


    def failure(parsed_args):
        logger.critical('failure message')
        msg_type = 'failure'
        return msg_type


    def worker_func(parsed_args, config, tell_manager):
        ...
        return checklist


    if __name__ == '__main__':
        main()

Lines 1 through 5 are the module's triple-quoted docstring.
It will appear in auto-generated documentation of the module.
For convenience we will also use the docstring as the description element of the worker's command-line help message,
although that can easily be changed if you prefer to put more details in the docstring than you want to appear in the help text.

The minimum set of imports that a worker needs are:

.. code-block:: python

    import logging

    from nemo_nowcast import NowcastWorker

The :py:mod:`logging` module is a Python standard library module that provides the mechanism that we use to print output about the worker's progress and status to the log file or the screen,
effectively developer-approved print statements on steroids :-)
The :py:class:`~nemo_nowcast.worker.NowcastWorker` class provides the interface to the nowcast framework.

Obviously you will need to import whatever other modules your worker needs for its task.

Next up,
on lines 12 and 13,
are 2 module level variables:

.. code-block:: python

    NAME = 'worker_name'
    logger = logging.getLogger(NAME)

:py:data:`NAME` is used to identify the source of logging messages,
and messages exchanged between the worker and the nowcast manager process.

:py:data:`logger` is our interface to the Python standard library logging framework and we give this module's instance the worker's name.

Python scoping rules make module level variables available for use in any functions in the module without passing them as arguments but assigning new values to them elsewhere in the module will surely mess things up.


.. _WorkerMainFunction:

The :py:func:`main` Function
============================

The :py:func:`main` function is where our worker gets down to work.
It is called when the worker is run from the command line by virtue of the

.. code-block:: python

    if __name__ == '__main__':
        main()

stanza at the end of the module.

The minimum possible :py:func:`main` function is shown in lines 14 to 23:

.. code-block:: python

    def main():
        """Set up and run the worker.

        For command-line usage see:

        :command:`python -m nemo_nowcast.workers.worker_name --help`
        """
        worker = NowcastWorker(NAME, description=__doc__)
        worker.init_cli()
        worker.run(worker_func, success, failure)

The :py:func:`main` function docstring will appear in auto-generated documentation of the module.

First,
we create an instance of the :py:class:`~NEMO_Nowcast.worker.NowcastWorker` class that we call,
by convention,
:py:data:`worker`.
The :py:class:`~NEMO_Nowcast.worker.NowcastWorker` constructor takes 2 arguments:

* the :py:data:`NAME` that we defined as a module-level variable above
* a :py:data:`description` string that is used as the description element of the worker's command-line help message;
  here we use the worker's module docstring
  (that is automatically stored in the :py:data:`__doc__` module-level variable)

  The description part of the help message is the paragraph after the usage,
  for example:

  .. code-block:: bash

      (nowcast)$ python -m nowcast.workers.download_weather --help

  .. code-block:: none

      usage: python -m nowcast.workers.download_weather
             [-h] [--debug] [--yesterday] config_file {18,00,12,06}

      Salish Sea NEMO nowcast weather model dataset download worker. Download the
      GRIB2 files from today's 00, 06, 12, or 18 EC GEM 2.5km HRDPS operational
      model forecast.

      ...

See the :py:class:`NEMO_Nowcast.worker.NowcastWorker` documentation for details of the :py:class:`~NEMO_Nowcast.worker.NowcastWorker` object's contructor arguments,
other attributes,
and methods.

Next,
we call the :py:meth:`init_cli` method on the worker to initialize the worker's command-line interface (CLI).
The default worker command-line interface requires a nowcast config file name,
and provides :kbd:`--debug`,
:kbd:`--help`,
and :kbd:`-h` options.
The worker's CLI can be extended with additional command-line arguments and/or options.
Please see :ref:`ExtendingTheCommandLineInterface` for details.

Finally,
we call the :py:meth:`run` method on the :py:data:`worker` to do the actual work.
The :py:meth:`run` method takes 3 function names as arguments:

* :py:data:`worker_func` is the name of the function that does the worker's job
* :py:data:`success` is the name of the function to be called when the worker finishes successfully
* :py:data:`failure` is the name of the function to be called when the worker fails

All 3 functions must be defined in the worker module.
Their required call signatures and return values are described below.


.. _WorkerSuccessAndFailureFunctions:

:py:func:`success` and :py:func:`failure` Functions
===================================================

The :py:func:`success` function is called when the worker successfully completes its task.
It is used to generate the message that is sent to the nowcast manager process to indicate the worker's success so that the nowcast automation can proceed to the next appropriate worker(s).
A minimal :py:func:`success` function is shown in lines 26 through 29:

.. code-block:: python

    def success(parsed_args):
        logger.info('success message')
        msg_type = 'success'
        return msg_type

The name of the function is :py:func:`success` by convention,
but it could be anything provided that it is the 2nd argument passed to the :py:meth:`worker.run` method.

The :py:func:`success` function must accept exactly 1 argument,
named :py:data:`parsed_args` by convention.
It is an :py:obj:`argparse.Namespace` object that has the worker's command-line argument names and values as attributes.
Even if your :py:func:`success` function does not use :py:data:`parsed_args` it must still be included in the function definition.

The :py:func:`success` function should send a message via :py:meth:`logger.info` to the logging system that describes the worker's success.

The :py:func:`success` function must return a string that is a key registered for the worker in the :ref:`MessageRegistryConfig` section of the :ref:`NowcastConfigFile`.
The returned key specifies the message type that is sent to the :ref:`SystemManager` process to indicate the worker's success.

Here is a more sophisticated example of a :py:func:`success` function from the :ref:`GoMSS Nowcast package download_weather <gomssnowcast:DownloadWeatherWorker>`
 worker:

.. code-block:: python

    def success(parsed_args):
        logger.info(
            '{date} weather forecast file downloads complete'
            .format(date=parsed_args.forecast_date.format('YYYY-MM-DD')))
        msg_type = 'success'
        return msg_type

The :py:func:`failure` function is very similar to the :py:func:`success` function except that it is called if the worker fails to complete its task.
It is used to generate the message that is sent to the nowcast manager process to indicate the worker's failure so that appropriate notifications can be produced and/or remedial action(s) taken.
A minimal :py:func:`failure` function is shown on lines 32 through 35:

.. code-block:: python

    def failure(parsed_args):
        logger.critical('failure message')
        msg_type = 'failure'
        return msg_type

The name of the function is :py:func:`failure` by convention,
but it could be anything provided that it is the 3rd argument passed to the :py:meth:`worker.run` method.

Like the :py:func:`success` function,
the :py:func:`failure` function must accept exactly 1 argument,
named :py:data:`parsed_args` by convention.
It is an :py:obj:`argparse.Namespace` object that has the worker's command-line argument names and values as attributes.
Even if your :py:func:`failure` function does not use :py:data:`parsed_args` it must still be included in the function definition.

The :py:func:`failure` function should send a message via :py:meth:`logger.critical` to the logging system that describes the worker's failure.

The :py:func:`failure` function must return a string that is a key registered for the worker in the :ref:`MessageRegistryConfig` section of the :ref:`NowcastConfigFile`.
The returned key specifies the message type that is sent to the nowcast manager process to indicate the worker's failure.


.. _DoingTheWork:

Doing the Work
==============

Lines 38 through 40 show the required call signature and return value for the function that is called to do the worker's task:

.. code-block:: python

    def worker_func(parsed_args, config, tell_manager):
        ...
        return checklist

The name of the function can be anything provided that it is the 1st argument passed to the :py:meth:`worker.run` method.
Ideally,
the function name should be descriptive of the worker's task.
If you can't think of anything else,
you can use the name of the worker module.

The function must accept exactly 3 arguments:

* The 1st argument is named :py:data:`parsed_args` by convention.
  It is an :py:obj:`argparse.Namespace` object that has the worker's command-line argument names and values as attributes.
  Even if your function does not use :py:data:`parsed_args` it must still be included in the function definition.

* The 2nd argument is named :py:data:`config` by convention.
  It is a :py:class:`nemo_nowcast.config.Config` object that provides :py:class:`dict`-like access to the nowcast system configuration loaded from the :ref:`NowcastConfigFile`.
  Even if your function does not use :py:data:`config` it must still be included in the function definition.

* The 3rd argument is named :py:data:`tell_manager` by convention.
  It is the worker's :py:meth:`nemo_nowcast.worker.NowcastWorker.tell_manager` method.
  That method provides a mechanism for the exchange of messages with the nowcast manager process.
  Few workers need to do that,
  so the :py:data:`tell_manager` is often replaced by :py:data:`*args` in the function signature:

  .. code-block:: python

    def worker_func(parsed_args, config, *args):

  Please see the :ref:`SalishSeaNowcast package watch_NEMO <salishseanowcast:WatchNEMO-Worker>` worker for examples of the use of :py:data:`tell_manager`.

The function must return a Python :py:obj:`dict`,
known as :py:data:`checklist` by convention.
:py:data:`checklist` must contain at least 1 key/value pair that provides information about the worker's successful completion.
:py:data:`checklist` is sent to the nowcast manager process as the payload of the worker's success message.
A simple example of a :py:data:`checklist` from the :ref:`GoMSS Nowcast package download_weather <gomssnowcast:DownloadWeatherWorker>` worker is:

.. code-block:: python

    checklist = {
        '{date} forecast'
        .format(date=date=parsed_args.forecast_date.format('YYYY-MM-DD'))): True}

which indicates that the particular forecast download was successful.
A more sophisticated :py:data:`checklist` such as the one produced by the :ref:`SalishSeaNowcast package get_NeahBay_ssh <salishseanowcast:GetNeahBaySshWorker>` worker contains multiple keys and lists of filenames.

The function whose name is passed as the 1st argument to the :py:meth:`worker.run` method can be a driver function that calls other functions in the worker module to subdivide the worker task into smaller,
more readable,
and more testable sections.
By convention,
such "2nd level" functions are marked as private by prefixing their names with the :kbd:`_` (underscore) character;
e.g. :py:func:`_calc_date`.
This is in line with the Python language convention that functions and methods that start with an underscore should not be called outside the module in which they are defined.

The worker should send messages to the logging system that indicate its progress.
Messages sent via :py:meth:`logger.info` appear in the :file:`nowcast.log` file.
Info level logging should be used for "high level" progress messages,
and preferably not used inside loops.
Messages logged via :py:meth:`logger.debug` can be used for more detailed logging.
Those messages appear in the :file:`nowcast.debug.log` file.

If a worker function encounters an expected error condition
(a file download failure or timeout, for example)
it should send a message to the logging system via :py:meth:`logger.critical` and raise a :py:exc:`nemo_nowcast.worker.WorkerError` exception.
Here is an example that handles an empty downloaded file in the :ref:`SalishSeaNowcast package download_weather <salishseanowcast:DownloadWeatherWorker>` worker:

.. code-block:: python

    if size == 0:
        logger.critical('Problem, 0 size file {}'.format(fileURL))
        raise WorkerError

This section has only outlined the basic code structure and conventions for writing nowcast workers.
The best way to learn now to write a new worker is by studying the code in existing worker modules,
for example:

* :ref:`BuiltinWorkers`
* :ref:`gomssnowcast:GoMSS_NowcastSystemWorkers`
* :ref:`salishseanowcast:SalishSeaNowcastSystemWorkers`


.. _ExtendingTheCommandLineInterface:

Extending the Command Line Interface
====================================

Generic Arguments
-----------------

If you need to add a command-line argument to a worker you can do so by calling the :py:meth:`worker.cli.add_argument` method.
Here is an example from the :ref:`SalishSeaNowcast package get_NeahBay_ssh <salishseanowcast:GetNeahBaySshWorker>` worker:

.. code-block:: python

    def main():
        """Set up and run the worker.

        For command-line usage see:

        :command:`python -m nowcast.workers.get_NeahBay_ssh --help`
        """
        worker = NowcastWorker(NAME, description=__doc__)
        worker.init_cli()
        worker.cli.add_argument(
            'run_type', choices={'nowcast', 'forecast', 'forecast2'},
            help="""
            Type of run to prepare open boundary sea surface height file for.
            """,
        )
        worker.run(get_NeahBay_ssh, success, failure)

The :py:meth:`worker.cli.add_argument` method is documented at :py:meth:`nemo_nowcast.cli.CommandLineInterface.add_argument`.
It takes the same arguments as the Python standard library :py:meth:`argparse.ArgumentParser.add_argument` method.

.. note::
    The :py:meth:`worker.init_cli` method initialized the worker's command-line interface to provide help messages,
    and handle the :kbd:`config_file` argument,
    and the :kbd:`--debug` option.


Date Options
------------

The fairly common need to add a date option to a worker's CLI is simplified by the :py:meth:`worker.cli.add_date_option`.
Here is an example from the :ref:`GoMSS Nowcast package download_weather <gomssnowcast:DownloadWeatherWorker>` worker:

.. code-block:: python

    def main():
        """Set up and run the worker.

        For command-line usage see:

        :command:`python -m nowcast.workers.download_weather --help`
        """
        worker = NowcastWorker(NAME, description=__doc__)
        worker.init_cli()
        worker.cli.add_date_option(
            '--forecast-date', default=arrow.now().floor('day'),
            help='Date for which to download the weather forecast.')
        worker.run(download_weather, success, failure)

This adds a :kbd:`--forecast-date` option to the CLI.
It's default value is an `Arrow`_ object whose value is midnight on the current date.
It will be available in the worker functions as :py:data:`parsed_args.forecast_date`.
The help message for the option is:

Date for which to download the weather forecast.
Use YYYY-MM-DD format. Defaults to {default}.

where :kbd:`{default}` is the value of :py:data:`default` passed into :py:meth:`worker.cli.add_date_option` formatted as YYYY-MM-DD.

.. _Arrow: http://crsmithdev.com/arrow/

The :py:meth:`worker.cli.add_date_option` method is documented at :py:meth:`nemo_nowcast.cli.CommandLineInterface.add_date_option`.

.. note::

    The `Arrow`_ object produced by :py:meth:`worker.cli.add_date_option` is timezone-aware and its timezone is set to UTC.
    That is typically fine when working with just the date.
    If you need to do time calculations in a worker you may need to set the correct timezone.
    That is typically done by calling the :py:meth:`to` method on the Arrow object with :kbd:`'local'` as its argument;
    e.g. :kbd:`parsed_args.forecast_date.to('local')`.
