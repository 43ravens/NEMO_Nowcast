**********
Change Log
**********

Next Release
============

These changes have been implemented and are in the
https://bitbucket.org/43ravens/nemo_nowcast code repository.

* Fix a bug whereby ``checklist.log`` file was neither being written nor being
  rotated.
  See `issue #9`_

  .. _issue #9: https://bitbucket.org/43ravens/nemo_nowcast/issues/9

* Added option to use ZeroMQ PUB/SUB sockets for distributed logging.
  See https://nemo-nowcast.readthedocs.io/en/latest/architecture/log_aggregator.html
  With this change the ``log`` message type is eliminated since it was a less
  flexible form of distributed logging.
  Nowcast systems with workers that use the ``log`` message type must be
  changed to use distributed logging.


v1.3
====

* Added option to set max retry waiting time to ``worker.get_web_data()``.
  See `issue #3`_

  .. _issue #3: https://bitbucket.org/43ravens/nemo_nowcast/issues/3

* ``rotate_logs`` worker sets permissions on newly created log files to
  ``rw-rw-r--``.

* The ``fileutils`` module from the Python `boltons`_ package has been added
  to the ``NEMO_Nowcast`` package as a vendored module.
  Please see the ``README.rst`` file for information about the copyright and
  license that apply to ``fileutils``.

  .. _boltons: https://boltons.readthedocs.io/en/latest/

* Replace logging ``RotatingFileHandler`` with ``WatchedFileHandler`` in logging
  setup of ``manager``, ``message_broker``, and ``scheduler`` so that they
  notice when log files are rotated and switch to writing to the new ones.
  See `issue #8`_

  .. _issue #8: https://bitbucket.org/43ravens/nemo_nowcast/issues/8

* Pass system state checklist dict into ``next_workers.after_*()`` calls so that
  ``after_*()`` functions can access it to define what workers to launch next
  and/or their order.
  See `issue #7`_

  .. _issue #7: https://bitbucket.org/43ravens/nemo_nowcast/issues/7


v1.2
====

* Add the ability to handle ``need`` and ``log`` message types to the
  manager.

* The configuration dict data structure has been removed from the
  ``Config.__repr__()`` output because, in practice, the data structure
  is many lines long and its inclusion renders the ``__repr__()`` method
  output almost unreadable.

* Change the ``scheduled worker`` configuration file section to be a list
  of dicts.
  This enables the same worker module to be scheduled for execution at several
  different times.
  For example,
  a ``download_weather`` worker can now be scheduled to run 4 times a day to
  get the products of each of the Environment Canada HRDPS model runs.

  **NOTE:** As a consequence of this change the ability to configure the
  time period between system clock checks that the scheduler uses has been
  removed.
  It is now hard-coded to 60 seconds.

* Make remote host worker launch process include sourcing a bash script that
  sets the nowcast system environment variables as a prefix to the worker
  launch command.
  The location of the script is defined in the config file.

* Enable worker.get_web_data() to return content, as an alternative to storing
  it at a file path.

* Fix a bug whereby workers write logging messages to all file handlers
  when ``--debug`` option is used instead of logging only to console.
  See `issue #2`_

  .. _issue #2: https://bitbucket.org/43ravens/nemo_nowcast/issues/2

* Pass system config dict into ``next_workers.after_*()`` calls so that
  ``after_*()`` functions can access it to define what workers to launch next
  and/or their order.
  See `issue #5`_

  .. _issue #5: https://bitbucket.org/43ravens/nemo_nowcast/issues/5

* Moved nemo_nowcast.NowcastWorker.add_argument() method to
  nemo_nowcast.CommandLineInterface class to make addition of arguments and
  options to worker CLIs consistently operate on worker.cli.
  See `issue #4`_

  .. _issue #4: https://bitbucket.org/43ravens/nemo_nowcast/issues/4

* Added this change log to the docs.
* Fixed bug in worker.get_web_data() function that caused an infinite loop to
  start after a waited-for file was finally downloaded.

v1.1
====

* Eliminated lib module by refactoring command-line argument parsing
  functions into attr.s-decorated nemo_nowcast.cli.CommandLineInterface
  class that is available in the nemo_nowcast namespace.
* Refactored system config data structure and lib.load_config() into
  attr.s-decorated nemo_nowcast.config.Config class that is available
  in the nemo_nowcat namespace.
* Added worker and message classes & worker.get_web_data() function
  to nemo_nowcast namespace.
* Refactored message data structure, lib.serialize_message(),
  and lib.deserialize_message() functions into attr.s-decorated
  nemo_nowcast.message.Message class.
* Refactored nemo_nowcast.manager.NowcastManager and
  nemo_nowcast.worker.NowcastWorker into attr.s-decorated classes.
* Add nemo_nowcast.worker.NowcastWorker.get_web_data() function to
  robustly download content from URLs via retries with exponential backoff.
* Refactored nemo_nowcast.workers.NextWorker into attr.s-decorated class
  with launch method moved in from lib module.
* Added arrow and attrs packages as dependencies
  (available from gomss-nowcast channel on anaconda.org).
* Fix bugs that arise when scheduled workers config is missing or empty.


v1.0
====

* Add worker launch scheduler module.
* Add clear_checklist built-in worker.
* Add rotate_logs built-in worker.
* Add framework documentation.
* Add example next_workers module.
* Add ability to substitute environment variable values into nowcast
  system YAML configuration file.
* Add sleep & awaken example nowcast worker modules.


v0.3
====

* Add nowcast worker module.


v0.2
====

* Start API docs.
* Add nowcast manager module.
* Start unit test suite.
* Start Sphinx docs with package development section.
* Add message broker module.


v0.1
====

* Initial release for packaging testing.
