**********
Change Log
**********

v25.1 (unreleased)
==================


v24.1 (2024-11-27)
==================

* Add support for Python 3.13.
  Change to Python 3.13 for development.
  Minimum supported Python version is 3.12.

* Add release process section to package development docs

* Modernize packaging:

  * Move conda environment description YAML files and :file:`requirements.txt` file from top
    level directory into :file:`envs/` subdirectory
  * Replace :file:`setup.py` with :file:`pyproject.toml`
  * Move `coverage`_ configuration from :file:`.coveragerc` to :file:`pyproject.toml`
  * Change from ``setuptools`` to hatch_ for build backend

  .. _coverage: https://coverage.readthedocs.io/en/latest/
  .. _hatch: https://hatch.pypa.io/

* Add pre-commit to manage code style and repo QA.

* Drop support for Python 3.10, and 3.11.
  Minimum supported Python version is now 3.12.


v22.1 (2023-01-23)
==================

* Drop support for Python 3.6, 3.7, 3.8, and 3.9.
  Minimum supported Python version is now 3.10.

* Add GitHub Actions `Sphinx linkcheck workflow`_ to monitor documentation for broken
  and redirected external links.

  .. _Sphinx linkcheck workflow: https://github.com/SalishSeaCast/SalishSeaCmd/actions?query=workflow%3Acodeql-analysis

* Add GitHub Actions `CodeQL analysis workflow`_ to monitor codebase for security
  vulnerabilities.

  .. _CodeQL analysis workflow: https://github.com/SalishSeaCast/SalishSeaCmd/actions?query=workflow%3Acodeql-analysis


v21.1 (2021-03-03)
==================

* End package releases on anaconda.org GoMSS-Nowcast channel.
  Final release there was v19.2

* Change name of Git repository default branch from ``master`` to ``main``.

* Add support for exception logging to Sentry (https://sentry.io/welcome/) with client DSN URL
  from SENTRY_DSN environment variable; does nothing if SENTRY_DSN does not exist,
  is empty, or is not recognized by Sentry.

* Change continuous integration from Bitbucket pipeline to GitHub Actions workflow.
  CI reports are at https://github.com/43ravens/NEMO_Nowcast/actions
  Unit test coverage report visualization is at https://app.codecov.io/gh/43ravens/NEMO_Nowcast

* Migrate from Mercurial on Bitbucket to Git on GitHub due to Bitbucket's decision
  to terminate support for Mercurial.
  Repository is now at https://github.com/43ravens/NEMO_Nowcast

* Expose ``nemo_nowcast.cli.arrow_date()`` function for use by packages like
  SalishSeaNowcast that use NEMO_Nowcast CLI elements.

* Change process manager from `circus`_ to `supervisor`_ because ``circus`` has
  dependency version pins that prevent moving to newer versions of Python and 0mq
  (and probably other packages).
  ``circus`` does not appear to be being actively maintained any more.
  ``supervisor`` has fewer dependencies, provides all of the functionality that we
  need, and is being actively maintained.

  .. _supervisor: https://supervisord.org/


v19.2 (2019-11-11)
==================

* Pin Python version at 3.6 and `circus`_ package version at 0.15 to ensure consistent
  conda environments due to dependency version pins in `circus`_.

  .. _circus: https://circus.readthedocs.io/en/latest/

* Allow remote workers to have a list of logging ports on each host to facilitate
  concurrent remote worker instances.

* Drop support for Python 3.5.

* Add worker race condition management.
  See https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/elements.html#handling-worker-race-conditions

* Add general and module indices to docs sidebar.

* Add Bitbucket continuous integration pipeline to run unit tests and generate unit
  tests coverage report.

* Add ability to send worker completion messages to a Slack channel via the
  `Slack incoming webhooks API`_.
  Documentation coming soon...

  .. _Slack incoming webhooks API: https://api.slack.com/messaging/webhooks


v19.1 (2019-01-17)
==================

* Change to `CalVer`_ versioning convention.
  Version identifier format is now ``yy.n[.devn]``,
  where ``yy`` is the (post-2000) year of release,
  and ``n`` is the number of the release within the year, starting at ``1``.
  After a release has been made the value of ``n`` is incremented by 1,
  and ``.dev0`` is appended to the version identifier to indicate changes that will be
  included in the next release.
  ``v18.1.dev0`` is an exception to that scheme.
  That version identifies the period of development between the ``v1.4`` and ``v19.1``
  releases.

  .. _CalVer: https://calver.org/

* Change to use `black`_ for code style management.

  .. _black: https://black.readthedocs.io/en/stable/

* Fix bug in ``get_web_data()`` re: calculation of total time of retries.
  Previously waiting would time out long before ``wait_exponential_max``.

* Add ``Config.__contains__()`` to enable checking for existence of top level keys in
  config.


v1.4 (2017-05-11)
=================

* Fix a bug whereby ``checklist.log`` file was neither being written nor being
  rotated.
  See `issue #9`_

  .. _issue #9: https://github.com/43ravens/NEMO_Nowcast/issues/9

* Added option to use ZeroMQ PUB/SUB sockets for distributed logging.
  See https://nemo-nowcast.readthedocs.io/en/latest/architecture/log_aggregator.html
  With this change the ``log`` message type is eliminated since it was a less
  flexible form of distributed logging.
  Nowcast systems with workers that use the ``log`` message type must be
  changed to use distributed logging.


v1.3 (2017-01-18)
=================

* Added option to set max retry waiting time to ``worker.get_web_data()``.
  See `issue #3`_

  .. _issue #3: https://github.com/43ravens/NEMO_Nowcast/issues/3

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

  .. _issue #8: https://github.com/43ravens/NEMO_Nowcast/issues/8

* Pass system state checklist dict into ``next_workers.after_*()`` calls so that
  ``after_*()`` functions can access it to define what workers to launch next
  and/or their order.
  See `issue #7`_

  .. _issue #7: https://github.com/43ravens/NEMO_Nowcast/issues/7


v1.2 (2016-10-19)
=================

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

  .. _issue #2: https://github.com/43ravens/NEMO_Nowcast/issues/2

* Pass system config dict into ``next_workers.after_*()`` calls so that
  ``after_*()`` functions can access it to define what workers to launch next
  and/or their order.
  See `issue #5`_

  .. _issue #5: https://github.com/43ravens/NEMO_Nowcast/issues/5

* Moved nemo_nowcast.NowcastWorker.add_argument() method to
  nemo_nowcast.CommandLineInterface class to make addition of arguments and
  options to worker CLIs consistently operate on worker.cli.
  See `issue #4`_

  .. _issue #4: https://github.com/43ravens/NEMO_Nowcast/issues/4

* Added this change log to the docs.
* Fixed bug in worker.get_web_data() function that caused an infinite loop to
  start after a waited-for file was finally downloaded.

v1.1 (2016-09-22)
=================

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


v1.0 (2016-08-18)
=================

* Add worker launch scheduler module.
* Add clear_checklist built-in worker.
* Add rotate_logs built-in worker.
* Add framework documentation.
* Add example next_workers module.
* Add ability to substitute environment variable values into nowcast
  system YAML configuration file.
* Add sleep & awaken example nowcast worker modules.


v0.3 (2016-06-25)
=================

* Add nowcast worker module.


v0.2 (2016-06-23)
=================

* Start API docs.
* Add nowcast manager module.
* Start unit test suite.
* Start Sphinx docs with package development section.
* Add message broker module.


v0.1
====

* Initial release for packaging testing.
