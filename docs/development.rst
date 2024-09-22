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

***************************************
:kbd:`NEMO_Nowcast` Package Development
***************************************

.. image:: https://img.shields.io/badge/license-Apache%202-cb2533.svg
    :target: https://www.apache.org/licenses/LICENSE-2.0
    :alt: Licensed under the Apache License, Version 2.0
.. image:: https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    :target: https://opensource.org/licenses/BSD-3-Clause
    :alt: Licensed under the BSD-3-Clause License
.. image:: https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&label=Python&logoColor=gold
    :target: https://docs.python.org/3.11/
    :alt: Python Version
.. image:: https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast
    :alt: Git on GitHub
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

.. image:: https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&label=Python&logoColor=gold
    :target: https://docs.python.org/3.11/
    :alt: Python Version


The :kbd:`SalishSeaNowcast` package is developed and tested using `Python`_ 3.11.

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
    $ conda env create -f environment-dev.yaml
    $ conda activate nemo-nowcast

The ``NEMO_Nowcast`` is installed in `editable install mode`_ as part of the conda environment
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

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://black.readthedocs.io/en/stable/
    :alt: The uncompromising Python code formatter

The :kbd:`NEMO_Nowcast` package uses the `black`_ code formatting tool to maintain a coding style that is very close to `PEP 8`_.

.. _black: https://black.readthedocs.io/en/stable/
.. _PEP 8: https://peps.python.org/pep-0008/

:command:`black` is installed as part of the :ref:`NEMO_NowcastDevelopmentEnvironment` setup.

To run :command:`black` on the entire code-base use:

.. code-block:: bash

    $ cd NEMO_Nowcast
    $ conda activate nemo-nowcast
    (nemo-nowcast)$ black ./

in the repository root directory.
The output looks something like::

  reformatted /media/doug/warehouse/MEOPAR/NEMO_Nowcast/nemo_nowcast/workers/clear_checklist.py
  reformatted /media/doug/warehouse/MEOPAR/NEMO_Nowcast/nemo_nowcast/config.py
  reformatted /media/doug/warehouse/MEOPAR/NEMO_Nowcast/tests/workers/test_clear_checklist.py
  reformatted /media/doug/warehouse/MEOPAR/NEMO_Nowcast/tests/test_config.py
  reformatted /media/doug/warehouse/MEOPAR/NEMO_Nowcast/nemo_nowcast/worker.py
  reformatted /media/doug/warehouse/MEOPAR/NEMO_Nowcast/tests/test_worker.py
  All done! ✨ 🍰 ✨
  6 files reformatted, 26 files left unchanged.


.. _NEMO_NowcastBuildingTheDocumentation:

Building the Documentation
==========================

.. image:: https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    :target: https://nemo-nowcast.readthedocs.io/en/latest/
    :alt: Documentation Status

The documentation for the :kbd:`NEMO_Nowcast` package is written in `reStructuredText`_ and converted to HTML using `Sphinx`_.
Creating a :ref:`NEMO_NowcastDevelopmentEnvironment` as described above includes the installation of Sphinx.
Building the documentation is driven by the :file:`docs/Makefile`.
With your :kbd:`nemo-nowcast` development environment activated,
use:

.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/

.. code-block:: bash

    (nemo-nowcast)$ (cd docs && make clean html)

to do a clean build of the documentation.
The output looks something like:

.. code-block:: text

    Removing everything under '_build'...
    Running Sphinx v5.3.0
    making output directory... done
    loading intersphinx inventory from https://docs.python.org/3/objects.inv...
    loading intersphinx inventory from https://gomss-nowcast-system.readthedocs.io/en/latest/objects.inv...
    loading intersphinx inventory from https://salishsea-nowcast.readthedocs.io/en/latest/objects.inv...
    building [mo]: targets for 0 po files that are out of date
    building [html]: targets for 18 source files that are out of date
    updating environment: [new config] 18 added, 0 changed, 0 removed
    reading sources... [100%] nowcast_system/workers
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [100%] nowcast_system/workers
    generating indices... genindex py-modindex done
    highlighting module code... [100%] nemo_nowcast.workers.sleep
    writing additional pages... search done
    copying images... [100%] architecture/MessageBroker.png
    copying static files... done
    copying extra files... done
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
With your :kbd:`nemo-nowcast` environment activated,
use:

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/docs/
    (nemo-nowcast) docs$ make linkcheck

The output looks something like:

.. code-block:: text

    Running Sphinx v5.3.0
    loading pickled environment... done
    building [mo]: targets for 0 po files that are out of date
    building [linkcheck]: targets for 18 source files that are out of date
    updating environment: 0 added, 0 changed, 0 removed
    looking for now-outdated files... none found
    preparing documents... done
    writing output... [  5%] CHANGES
    writing output... [ 11%] api
    writing output... [ 16%] architecture/index
    writing output... [ 22%] architecture/log_aggregator
    writing output... [ 27%] architecture/manager
    writing output... [ 33%] architecture/message_broker
    writing output... [ 38%] architecture/messaging
    writing output... [ 44%] architecture/scheduler
    writing output... [ 50%] architecture/worker
    writing output... [ 55%] development
    writing output... [ 61%] index
    writing output... [ 66%] nowcast_system/builtin-workers
    writing output... [ 72%] nowcast_system/config
    writing output... [ 77%] nowcast_system/elements
    writing output... [ 83%] nowcast_system/index
    writing output... [ 88%] nowcast_system/process_mgmt
    writing output... [ 94%] nowcast_system/toy-example
    writing output... [100%] nowcast_system/workers


    (nowcast_system/workers: line  439) ok        https://arrow.readthedocs.io/en/latest/
    (         CHANGES: line   45) ok        http://supervisord.org/
    (         CHANGES: line   99) ok        https://black.readthedocs.io/en/stable/
    (         CHANGES: line  138) ok        https://boltons.readthedocs.io/en/latest/
    (         CHANGES: line   34) ok        https://app.codecov.io/gh/43ravens/NEMO_Nowcast
    (     development: line  520) ok        https://boltons.readthedocs.io/en/latest/fileutils.html
    (         CHANGES: line   45) ok        https://circus.readthedocs.io/en/latest/
    (     development: line  424) ok        https://coverage.readthedocs.io/en/latest/
    (         CHANGES: line   76) ok        https://api.slack.com/messaging/webhooks
    (     development: line   20) ok        https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg
    (     development: line  469) ok        https://docs.github.com/en/actions
    (     development: line   97) ok        https://docs.conda.io/en/latest/
    (         CHANGES: line   86) ok        https://calver.org/
    (     development: line   97) ok        https://docs.conda.io/en/latest/miniconda.html
    (     development: line  385) ok        https://docs.pytest.org/en/latest/
    (     development: line   20) ok        https://docs.python.org/3.11/
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    (             api: line    3) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.Namespace
    (             api: line    1) ok        https://docs.python.org/3/library/collections.html#collections.namedtuple
    (nowcast_system/toy-example: line   40) ok        https://anaconda.org/GoMSS-Nowcast/nemo_nowcast
    (             api: line   22) ok        https://docs.python.org/3/library/constants.html#None
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#False
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#True
    (             api: line    1) ok        https://docs.python.org/3/library/functions.html#float
    (             api: line    1) ok        https://docs.python.org/3/library/functions.html#int
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    (             api: line    3) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    (nowcast_system/config: line   58) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.WatchedFileHandler
    (             api: line    1) ok        https://docs.python.org/3/library/logging.html#logging.Logger
    (nowcast_system/elements: line   90) ok        https://docs.python.org/3/library/logging.html#logging.debug
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.html#module-logging
    (             api: line    1) ok        https://docs.python.org/3/library/pathlib.html#pathlib.Path
    (             api: line    1) ok        https://docs.python.org/3/library/stdtypes.html#bytes
    (             api: line    1) ok        https://docs.python.org/3/library/stdtypes.html#list
    (             api: line    3) ok        https://docs.python.org/3/library/stdtypes.html#dict
    (             api: line    1) ok        https://docs.python.org/3/library/stdtypes.html#str
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/stdtypes.html#tuple
    (nowcast_system/toy-example: line  194) ok        https://en.wikipedia.org/wiki/INI_file
    (nowcast_system/elements: line   73) ok        https://docs.python.org/3/library/stdtypes.html#set
    (     development: line  483) ok        https://git-scm.com/
    (architecture/worker: line   29) ok        https://en.wikipedia.org/wiki/Idempotence
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Acodeql-analysis
    (         CHANGES: line   38) ok        https://github.com/43ravens/NEMO_Nowcast
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Apytest-with-coverage
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/issues
    (         CHANGES: line   34) ok        https://github.com/43ravens/NEMO_Nowcast/actions
    (     development: line  458) ok        https://github.com/43ravens/NEMO_Nowcast/commits/main
    (         CHANGES: line  192) ok        https://github.com/43ravens/NEMO_Nowcast/issues/2
    (         CHANGES: line  205) ok        https://github.com/43ravens/NEMO_Nowcast/issues/4
    (         CHANGES: line  130) ok        https://github.com/43ravens/NEMO_Nowcast/issues/3
    (         CHANGES: line  198) ok        https://github.com/43ravens/NEMO_Nowcast/issues/5
    (         CHANGES: line  152) ok        https://github.com/43ravens/NEMO_Nowcast/issues/7
    (         CHANGES: line  145) ok        https://github.com/43ravens/NEMO_Nowcast/issues/8
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/sphinx-linkcheck/badge.svg
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/pytest-with-coverage/badge.svg
    (           index: line   48) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/index.html
    (nowcast_system/workers: line  246) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (         CHANGES: line  113) ok        https://github.com/43ravens/NEMO_Nowcast/issues/9
    (nowcast_system/workers: line   43) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#gomss-nowcastsystemworkers
    (         CHANGES: line   11) ok        https://github.com/SalishSeaCast/SalishSeaCmd/actions?query=workflow%3Acodeql-analysis
    (nowcast_system/elements: line   24) ok        https://github.com/SalishSeaCast/SalishSeaNowcast
    (     development: line  520) ok        https://github.com/mahmoud/boltons/blob/master/LICENSE
    (     development: line   20) ok        https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&label=Python&logoColor=gold
    (     development: line   20) ok        https://img.shields.io/badge/code%20style-black-000000.svg
    (architecture/message_broker: line   48) ok        https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html
    (     development: line   20) ok        https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    (     development: line   20) ok        https://img.shields.io/badge/license-Apache%202-cb2533.svg
    (     development: line   20) ok        https://nemo-nowcast.readthedocs.io/en/latest/
    (         CHANGES: line  119) ok        https://nemo-nowcast.readthedocs.io/en/latest/architecture/log_aggregator.html
    (     development: line   20) ok        https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    (         CHANGES: line   68) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/elements.html#handling-worker-race-conditions
    (             api: line    3) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/index.html
    (     development: line  112) ok        https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    (     development: line  520) ok        https://pypi.org/project/boltons/
    (     development: line   20) ok        https://opensource.org/licenses/BSD-3-Clause
    (     development: line  424) ok        https://pytest-cov.readthedocs.io/en/latest/
    (     development: line  135) ok        https://peps.python.org/pep-0008/
    (     development: line   20) ok        https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    (architecture/messaging: line  127) ok        https://pyyaml.org/wiki/PyYAMLDocumentation
    (           index: line   30) ok        https://salishsea-nowcast.readthedocs.io/en/latest/
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadliveoceanworker
    (nowcast_system/workers: line  354) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#gribtonetcdfworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makeliveoceanfilesworker
    (nowcast_system/workers: line  336) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makesshfilesworker
    (     development: line   20) ok        https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    (             api: line    3) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.next_workers
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#process-flow
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#nowcast.next_workers.after_collect_weather
    (nowcast_system/workers: line   44) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#salishseanowcastsystemworkers
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#uploadforcingworker
    (nowcast_system/workers: line  322) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#watchnemo-worker
    (     development: line   20) ok        https://www.apache.org/licenses/LICENSE-2.0
    (           index: line   43) ok        https://salishsea.eos.ubc.ca/nemo/results/index.html
    (     development: line  172) ok        https://www.sphinx-doc.org/en/master/
    (     development: line   66) ok        https://www.python.org/
    (architecture/messaging: line   47) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.workers.download_weather
    (     development: line  172) ok        https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
    (architecture/message_broker: line   48) ok        https://zeromq.org/
    (         CHANGES: line   30) ok        https://sentry.io/welcome/
    (           index: line   21) ok        https://www.nemo-ocean.eu/
    build succeeded.

    Look for any errors in the above output or in _build/html/output.txt

:command:`make linkcheck` is run monthly via a `scheduled GitHub Actions workflow`_

.. _scheduled GitHub Actions workflow: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck


.. _NEMO_NowcastRunningTheUnitTests:

Running the Unit Tests
======================

The test suite for the :kbd:`NEMO_Nowcast` package is in :file:`NEMO_Nowcast/tests/`.
The `pytest`_ tool is used for test parametrization and as the test runner for the suite.

.. _pytest: https://docs.pytest.org/en/latest/

With your :kbd:`nemo-nowcast` development environment activated,
use:

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/
    (nemo-nowcast)$ pytest

to run the test suite.
The output looks something like::

  ============================ test session starts ============================
  platform linux -- Python 3.6.7, pytest-4.0.1, py-1.7.0, pluggy-0.8.1
  rootdir: /media/doug/warehouse/43ravens/projects/gomss-nowcast/NEMO_Nowcast, inifile:
  collected 300 items

  tests/test_cli.py .................                                                       [  5%]
  tests/test_config.py .............                                                        [ 10%]
  tests/test_log_aggregator.py .................                                            [ 15%]
  tests/test_manager.py ...............................................................
  ...................                                                                       [ 43%]
  tests/test_message.py ......                                                              [ 45%]
  tests/test_message_broker.py ...................                                          [ 51%]
  tests/test_next_workers.py ......                                                         [ 53%]
  tests/test_scheduler.py ...................                                               [ 59%]
  tests/test_worker.py ................................................................
  ..............                                                                            [ 85%]
  tests/workers/test_awaken.py ........                                                     [ 88%]
  tests/workers/test_clear_checklist.py .........                                           [ 91%]
  tests/workers/test_rotate_logs.py .................                                       [ 97%]
  tests/workers/test_sleep.py .........                                                     [100%]

  ========================= 300 passed in 16.77 seconds =========================

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

The :kbd:`NEMO_Nowcast` package unit test suite is run and a coverage report is generated whenever changes are pushed to GitHub.
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

The :kbd:`NEMO_Nowcast` package code and documentation source files are available as a `Git`_ repository at https://github.com/43ravens/NEMO_Nowcast.

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
    :target: https://opensource.org/licenses/BSD-3-Clause
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
