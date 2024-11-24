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


.. _NEMO_NowcastPackageDevelopment:

******************************************
:py:obj:`NEMO_Nowcast` Package Development
******************************************

.. image:: https://img.shields.io/badge/license-Apache%202-cb2533.svg
    :target: https://www.apache.org/licenses/LICENSE-2.0
    :alt: Licensed under the Apache License, Version 2.0
.. image:: https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    :target: https://opensource.org/license/BSD-3-Clause
    :alt: Licensed under the BSD-3-Clause License
.. image:: https://img.shields.io/badge/Python-3.12-blue?logo=python&label=Python&logoColor=gold
    :target: https://docs.python.org/3.12/
    :alt: Python Version
.. image:: https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast
    :alt: Git on GitHub
.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://pre-commit.com
    :alt: pre-commit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://black.readthedocs.io/en/stable/
    :alt: The uncompromising Python code formatter
.. image:: https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    :target: https://nemo-nowcast.readthedocs.io/en/latest/
    :alt: Documentation Status
.. image:: https://github.com/43ravens/NEMO_Nowcast/workflows/sphinx-linkcheck/badge.svg
    :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck
    :alt: Sphinx linkcheck
.. image:: https://github.com/43ravens/NEMO_Nowcast/workflows/pytest-with-coverage/badge.svg
    :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Apytest-with-coverage
    :alt: Pytest with Coverage Status
.. image:: https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg
    :target: https://app.codecov.io/gh/43ravens/NEMO_Nowcast
    :alt: Codecov Testing Coverage Report
.. image:: https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg
    :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Acodeql-analysis
    :alt: CodeQL analysis
.. image:: https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast/issues
    :alt: Issue Tracker

.. _NEMO_NowcastPythonVersions:

Python Versions
===============

.. image:: https://img.shields.io/badge/Python-3.12-blue?logo=python&label=Python&logoColor=gold
    :target: https://docs.python.org/3.12/
    :alt: Python Version


The :py:obj:`NEMO_Nowcast` package is developed and tested using `Python`_ 3.12.

.. _Python: https://www.python.org/


.. _NEMO_NowcastGettingTheCode:

Getting the Code
================

.. image:: https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast
    :alt: Git on GitHub

Clone the code and documentation `repository`_ from GitHub with:

.. _repository: https://github.com/43ravens/NEMO_Nowcast

.. code-block:: bash

    $ git clone git@github.com:43ravens/NEMO_Nowcast.git


.. _NEMO_NowcastDevelopmentEnvironment:

Development Environment
=======================

Setting up an isolated development environment using `Conda`_ is recommended.
Assuming that you have `Miniconda3`_ installed,
you can create and activate an environment called ``nemo-nowcast`` that will have all of the Python packages necessary for development,
testing,
and building the documentation with the commands:

.. _Conda: https://docs.conda.io/en/latest/
.. _Miniconda3: https://docs.conda.io/en/latest/miniconda.html

.. code-block:: bash

    $ cd  NEMO_Nowcast
    $ conda env create -f envs/environment-dev.yaml
    $ conda activate nemo-nowcast

The :py:obj:`NEMO_Nowcast` package is installed in `editable install mode`_ as part of the conda environment
creation process.
That means that the package is installed from the cloned repo in such a way that
it call be updated as the repo evolves with a simple :command:`git pull`.

.. _editable install mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs

To deactivate the environment use:

.. code-block:: bash

    (nemo-nowcast)$ conda deactivate


.. _NEMO_NowcastCodingStyle:

Coding Style
============

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://pre-commit.com
    :alt: pre-commit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://black.readthedocs.io/en/stable/
    :alt: The uncompromising Python code formatter

The :py:obj:`NEMO_Nowcast` package uses the Git pre-commit hooks managed by `pre-commit`_
to maintain consistent code style and and other aspects of code,
docs,
and repo QA.

.. _pre-commit: https://pre-commit.com/

To install the ``pre-commit`` hooks in a newly cloned repo,
activate the conda development environment,
and run :command:`pre-commit install`:

.. code-block:: bash
    $ cd NEMO_Nowcast
    $ conda activate nemo-nowcast
    (nemo-nowcast)$ pre-commit install

.. note::
    You only need to install the hooks once immediately after you make a new clone of the
    `NEMO_Nowcast repository`_ and build your :ref:`NEMO_NowcastDevelopmentEnvironment`.

.. _NEMO_Nowcast repository: https://github.com/43ravens/NEMO_Nowcast


.. _NEMO_NowcastBuildingTheDocumentation:

Building the Documentation
==========================

.. image:: https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    :target: https://nemo-nowcast.readthedocs.io/en/latest/
    :alt: Documentation Status

The documentation for the :py:obj:`NEMO_Nowcast` package is written in `reStructuredText`_ and converted to HTML using `Sphinx`_.
Creating a :ref:`NEMO_NowcastDevelopmentEnvironment` as described above includes the installation of Sphinx.
Building the documentation is driven by the :file:`docs/Makefile`.
With your ``nemo-nowcast`` development environment activated,
use:

.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/

.. code-block:: bash

    (nemo-nowcast)$ (cd docs && make clean html)

to do a clean build of the documentation.
The output looks something like:

.. code-block:: text

    Removing everything under '_build'...
    Running Sphinx v8.1.3
    loading translations [en]... done
    making output directory... done
    Converting `source_suffix = '.rst'` to `source_suffix = {'.rst': 'restructuredtext'}`.
    loading intersphinx inventory 'python' from https://docs.python.org/3/objects.inv ...
    loading intersphinx inventory 'gomssnowcast' from https://gomss-nowcast-system.readthedocs.io/en/latest/objects.inv ...
    loading intersphinx inventory 'salishseanowcast' from https://salishsea-nowcast.readthedocs.io/en/latest/objects.inv ...
    building [mo]: targets for 0 po files that are out of date
    writing output...
    building [html]: targets for 18 source files that are out of date
    updating environment: [new config] 18 added, 0 changed, 0 removed
    reading sources... [100%] nowcast_system/workers
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    copying assets...
    copying static files...
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/language_data.js
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/basic.css
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/documentation_options.js
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/js/versions.js
    copying static files: done
    copying extra files...
    copying extra files: done
    copying assets: done
    writing output... [100%] nowcast_system/workers
    generating indices... genindex py-modindex done
    highlighting module code... [100%] nemo_nowcast.workers.sleep
    writing additional pages... search done
    copying images... [100%] architecture/MessageBroker.png
    dumping search index in English (code: en)... done
    dumping object inventory... done
    build succeeded.

    The HTML pages are in _build/html.

The HTML rendering of the docs ends up in :file:`docs/_build/html/`.
You can open the :file:`index.html` file in that directory tree in your browser to preview the results of the build.

If you have write access to the `repository`_ on GitHub,
whenever you push changes to GitHub the documentation is automatically re-built and rendered at https://nemo-nowcast.readthedocs.io/en/latest/.


.. _NEMO_NowcastLinkCheckingTheDocumentation:

Link Checking the Documentation
-------------------------------

.. image:: https://github.com/43ravens/NEMO_Nowcast/workflows/sphinx-linkcheck/badge.svg
    :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck
    :alt: Sphinx linkcheck

Sphinx also provides a link checker utility which can be run to find broken or redirected links in the docs.
With your ``nemo-nowcast`` environment activated,
use:

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/docs/
    (nemo-nowcast) docs$ make linkcheck

The output looks something like:

.. code-block:: text

    Removing everything under '_build'...
    Running Sphinx v8.1.3
    loading translations [en]... done
    making output directory... done
    Converting `source_suffix = '.rst'` to `source_suffix = {'.rst': 'restructuredtext'}`.
    loading intersphinx inventory 'python' from https://docs.python.org/3/objects.inv ...
    loading intersphinx inventory 'gomssnowcast' from https://gomss-nowcast-system.readthedocs.io/en/latest/objects.inv ...
    loading intersphinx inventory 'salishseanowcast' from https://salishsea-nowcast.readthedocs.io/en/latest/objects.inv ...
    building [mo]: targets for 0 po files that are out of date
    writing output...
    building [linkcheck]: targets for 18 source files that are out of date
    updating environment: [new config] 18 added, 0 changed, 0 removed
    reading sources... [100%] nowcast_system/workers
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    copying assets...
    copying assets: done
    writing output... [100%] nowcast_system/workers

    (nowcast_system/workers: line  439) ok        https://arrow.readthedocs.io/en/latest/
    (         CHANGES: line   52) ok        http://supervisord.org/
    (         CHANGES: line   41) ok        https://app.codecov.io/gh/43ravens/NEMO_Nowcast
    (         CHANGES: line  106) ok        https://black.readthedocs.io/en/stable/
    (         CHANGES: line  145) ok        https://boltons.readthedocs.io/en/latest/
    (     development: line  523) ok        https://boltons.readthedocs.io/en/latest/fileutils.html
    (         CHANGES: line   83) ok        https://api.slack.com/messaging/webhooks
    (         CHANGES: line   52) ok        https://circus.readthedocs.io/en/latest/
    (nowcast_system/toy-example: line   40) ok        https://anaconda.org/GoMSS-Nowcast/nemo_nowcast
    (     development: line  427) ok        https://coverage.readthedocs.io/en/latest/
    (     development: line   94) ok        https://docs.conda.io/en/latest/miniconda.html
    (     development: line   46) ok        https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg
    (     development: line   94) ok        https://docs.conda.io/en/latest/
    (         CHANGES: line   93) ok        https://calver.org/
    (     development: line  472) ok        https://docs.github.com/en/actions
    (     development: line  388) ok        https://docs.pytest.org/en/latest/
    (     development: line   20) ok        https://docs.python.org/3.12/
    (             api: line   70) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    (             api: line    3) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#False
    (             api: line  124) ok        https://docs.python.org/3/library/collections.html#collections.namedtuple
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.Namespace
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentTypeError
    (             api: line   22) ok        https://docs.python.org/3/library/constants.html#None
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#True
    (             api: line   61) ok        https://docs.python.org/3/library/functions.html#int
    (             api: line   61) ok        https://docs.python.org/3/library/functions.html#float
    (nowcast_system/config: line   58) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.WatchedFileHandler
    (             api: line    3) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    (architecture/manager: line   89) ok        https://docs.python.org/3/library/logging.html#logging.CRITICAL
    (             api: line   61) ok        https://docs.python.org/3/library/logging.html#logging.Logger
    (architecture/manager: line   53) ok        https://docs.python.org/3/library/logging.html#logging.ERROR
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.html#module-logging
    (nowcast_system/elements: line   90) ok        https://docs.python.org/3/library/logging.html#logging.debug
    (             api: line   25) ok        https://docs.python.org/3/library/pathlib.html#pathlib.Path
    (             api: line   61) ok        https://docs.python.org/3/library/stdtypes.html#bytes
    (             api: line  124) ok        https://docs.python.org/3/library/stdtypes.html#list
    (             api: line   34) ok        https://docs.python.org/3/library/stdtypes.html#str
    (             api: line    3) ok        https://docs.python.org/3/library/stdtypes.html#dict
    (nowcast_system/elements: line   73) ok        https://docs.python.org/3/library/stdtypes.html#set
    (     development: line  486) ok        https://git-scm.com/
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/stdtypes.html#tuple
    (nowcast_system/toy-example: line  194) ok        https://en.wikipedia.org/wiki/INI_file
    (architecture/worker: line   29) ok        https://en.wikipedia.org/wiki/Idempotence
    (     development: line   49) ok        https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Acodeql-analysis
    (         CHANGES: line   45) ok        https://github.com/43ravens/NEMO_Nowcast
    (         CHANGES: line   41) ok        https://github.com/43ravens/NEMO_Nowcast/actions
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/issues
    (         CHANGES: line  199) ok        https://github.com/43ravens/NEMO_Nowcast/issues/2
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Apytest-with-coverage
    (         CHANGES: line  137) ok        https://github.com/43ravens/NEMO_Nowcast/issues/3
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck
    (         CHANGES: line  205) ok        https://github.com/43ravens/NEMO_Nowcast/issues/5
    (         CHANGES: line  159) ok        https://github.com/43ravens/NEMO_Nowcast/issues/7
    (         CHANGES: line  212) ok        https://github.com/43ravens/NEMO_Nowcast/issues/4
    (     development: line  461) ok        https://github.com/43ravens/NEMO_Nowcast/commits/main
    (     development: line   40) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/sphinx-linkcheck/badge.svg
    (         CHANGES: line  152) ok        https://github.com/43ravens/NEMO_Nowcast/issues/8
    (     development: line   43) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/pytest-with-coverage/badge.svg
    (           index: line   48) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/index.html
    (         CHANGES: line  120) ok        https://github.com/43ravens/NEMO_Nowcast/issues/9
    (         CHANGES: line   18) ok        https://github.com/SalishSeaCast/SalishSeaCmd/actions?query=workflow%3Acodeql-analysis
    (nowcast_system/workers: line  245) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (nowcast_system/workers: line   43) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#gomss-nowcastsystemworkers
    (     development: line   34) ok        https://img.shields.io/badge/code%20style-black-000000.svg
    (     development: line  523) ok        https://github.com/mahmoud/boltons/blob/master/LICENSE
    (     development: line   28) ok        https://img.shields.io/badge/Python-3.12-blue?logo=python&label=Python&logoColor=gold
    (     development: line   22) ok        https://img.shields.io/badge/license-Apache%202-cb2533.svg
    (     development: line   31) ok        https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    (nowcast_system/elements: line   24) ok        https://github.com/SalishSeaCast/SalishSeaNowcast
    (architecture/message_broker: line   48) ok        https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html
    (     development: line   25) ok        https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    (     development: line   20) ok        https://nemo-nowcast.readthedocs.io/en/latest/
    (         CHANGES: line  126) ok        https://nemo-nowcast.readthedocs.io/en/latest/architecture/log_aggregator.html
    (     development: line   52) ok        https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    (     development: line  132) ok        https://peps.python.org/pep-0008/
    (         CHANGES: line   75) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/elements.html#handling-worker-race-conditions
    (             api: line    3) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/index.html
    (     development: line  523) ok        https://pypi.org/project/boltons/
    (     development: line   20) ok        https://opensource.org/license/BSD-3-Clause
    (     development: line  427) ok        https://pytest-cov.readthedocs.io/en/latest/
    (architecture/messaging: line  127) ok        https://pyyaml.org/wiki/PyYAMLDocumentation
    (     development: line  109) ok        https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    (           index: line   30) ok        https://salishsea-nowcast.readthedocs.io/en/latest/
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadliveoceanworker
    (nowcast_system/workers: line  354) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (     development: line   37) ok        https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#gribtonetcdfworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makeliveoceanfilesworker
    (nowcast_system/workers: line  336) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makesshfilesworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#process-flow
    (architecture/messaging: line   47) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.workers.download_weather
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#nowcast.next_workers.after_collect_weather
    (nowcast_system/workers: line   44) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#salishseanowcastsystemworkers
    (             api: line    3) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.next_workers
    (     development: line   20) ok        https://www.apache.org/licenses/LICENSE-2.0
    (         CHANGES: line   37) ok        https://sentry.io/welcome/
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#uploadforcingworker
    (           index: line   43) ok        https://salishsea.eos.ubc.ca/nemo/results/index.html
    (nowcast_system/workers: line  322) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#watchnemo-worker
    (     development: line  169) ok        https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
    (     development: line   66) ok        https://www.python.org/
    (     development: line  169) ok        https://www.sphinx-doc.org/en/master/
    (architecture/message_broker: line   48) ok        https://zeromq.org/
    (           index: line   21) ok        https://www.nemo-ocean.eu/
    build succeeded.

    Look for any errors in the above output or in _build/linkcheck/output.txt

:command:`make linkcheck` is run monthly via a `scheduled GitHub Actions workflow`_

.. _scheduled GitHub Actions workflow: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck


.. _NEMO_NowcastRunningTheUnitTests:

Running the Unit Tests
======================

The test suite for the :py:obj:`NEMO_Nowcast` package is in :file:`NEMO_Nowcast/tests/`.
The `pytest`_ tool is used for test parametrization and as the test runner for the suite.

.. _pytest: https://docs.pytest.org/en/latest/

With your ``nemo-nowcast`` development environment activated,
use:

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/
    (nemo-nowcast)$ pytest

to run the test suite.
The output looks something like:

.. code-block:: text

(/home/doug/conda_envs/nemo-nowcast) /media/doug/warehouse/43ravens/projects/NEMO_Nowcast git:[main]
pytest
================================== test session starts ===================================
platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
Using --randomly-seed=202895674
rootdir: /media/doug/warehouse/43ravens/projects/NEMO_Nowcast
plugins: randomly-3.15.0, cov-5.0.0
collected 319 items

tests/test_worker.py ....................................................................
........................                                                           [ 28%]
tests/workers/test_clear_checklist.py .........                                    [ 31%]
tests/test_scheduler.py ...................                                        [ 37%]
tests/workers/test_awaken.py ........                                              [ 40%]
tests/test_manager.py ...................................................................
................                                                                   [ 66%]
tests/test_cli.py .................                                                [ 71%]
tests/test_log_aggregator.py .................                                     [ 76%]
tests/test_next_workers.py ......                                                  [ 78%]
tests/workers/test_sleep.py .........                                              [ 81%]
tests/test_message.py ......                                                       [ 83%]
tests/test_config.py .................                                             [ 88%]
tests/test_message_broker.py ...................                                   [ 94%]
tests/workers/test_rotate_logs.py .................                                [100%]

================================== 319 passed in 18.69s ==================================

You can monitor what lines of code the test suite exercises using the `coverage.py`_ and `pytest-cov`_ tools with the commands:

.. _coverage.py: https://coverage.readthedocs.io/en/latest/
.. _pytest-cov: https://pytest-cov.readthedocs.io/en/latest/

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/
    (nemo-nowcast)$ pytest --cov=./

The test coverage report will be displayed below the test suite run output.

Alternatively,
you can use

.. code-block:: bash

    (nemo-nowcast)$ pytest --cov=./ --cov-report html

to produce an HTML report that you can view in your browser by opening :file:`NEMO_Nowcast/htmlcov/index.html`.


.. _NEMO_NowcastContinuousIntegration:

Continuous Integration
----------------------

.. image:: https://github.com/43ravens/NEMO_Nowcast/workflows/pytest-with-coverage/badge.svg
    :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Apytest-with-coverage
    :alt: Pytest with Coverage Status
.. image:: https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg
    :target: https://app.codecov.io/gh/43ravens/NEMO_Nowcast
    :alt: Codecov Testing Coverage Report

The :py:obj:`NEMO_Nowcast` package unit test suite is run and a coverage report is generated whenever changes are pushed to GitHub.
The results are visible on the `repo actions page`_,
from the green checkmarks beside commits on the `repo commits page`_,
or from the green checkmark to the left of the "Latest commit" message on the `repo code overview page`_ .
The testing coverage report is uploaded to `codecov.io`_

.. _repo actions page: https://github.com/43ravens/NEMO_Nowcast/actions
.. _repo commits page: https://github.com/43ravens/NEMO_Nowcast/commits/main
.. _repo code overview page: https://github.com/43ravens/NEMO_Nowcast
.. _codecov.io: https://app.codecov.io/gh/43ravens/NEMO_Nowcast

The `GitHub Actions`_ workflow configuration that defines the continuous integration tasks is in the :file:`.github/workflows/pytest-with-coverage.yaml` file.

.. _GitHub Actions: https://docs.github.com/en/actions


.. _NEMO_NowcastVersionControlRepository:

Version Control Repository
==========================

.. image:: https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast
    :alt: Git on GitHub

The :py:obj:`NEMO_Nowcast` package code and documentation source files are available as a `Git`_ repository at https://github.com/43ravens/NEMO_Nowcast.

.. _Git: https://git-scm.com/


.. _NEMO_NowcastIssueTracker:

Issue Tracker
=============

.. image:: https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast/issues
    :alt: Issue Tracker

Development tasks,
bug reports,
and enhancement ideas are recorded and managed in the issue tracker at https://github.com/43ravens/NEMO_Nowcast/issues


.. _NEMO_NowcastLicenses:

Licenses
========

.. image:: https://img.shields.io/badge/license-Apache%202-cb2533.svg
    :target: https://www.apache.org/licenses/LICENSE-2.0
    :alt: Licensed under the Apache License, Version 2.0
.. image:: https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    :target: https://opensource.org/license/BSD-3-Clause
    :alt: Licensed under the BSD-3-Clause License

The NEMO_Nowcast framework code and documentation are copyright 2016-2021 by Doug Latornell, 43ravens.

They are licensed under the Apache License, Version 2.0.
https://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.

The `fileutils`_ module from the `boltons`_ project is included in the NEMO_Nowcast package.
It is copyright 2016 by Mahmoud Hashemi and used under the terms of the `boltons BSD license`_.

.. _fileutils: https://boltons.readthedocs.io/en/latest/fileutils.html
.. _boltons: https://pypi.org/project/boltons/
.. _boltons BSD license: https://github.com/mahmoud/boltons/blob/master/LICENSE
