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
    :target: https://codecov.io/gh/43ravens/NEMO_Nowcast
    :alt: Codecov Testing Coverage Report
.. image:: https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg
      :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Acodeql-analysis
      :alt: CodeQL analysis
.. image:: https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast/issues
    :alt: Issue Tracker
.. image:: https://anaconda.org/gomss-nowcast/nemo_nowcast/badges/installer/conda.svg
    :target: https://conda.anaconda.org/gomss-nowcast
    :alt: Install with conda

.. _NEMO_NowcastPythonVersions:

Python Versions
===============

.. image:: https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&label=Python&logoColor=gold
    :target: https://docs.python.org/3.11/
    :alt: Python Version


The :kbd:`SalishSeaNowcast` package is developed and tested using `Python`_ 3.11.
The minimum supported Python version is 3.10.
The :ref:`NEMO_NowcastContinuousIntegration` workflow on GitHub ensures that the package
is tested for all versions of Python>=3.10.

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

or

.. code-block:: bash

    $ git clone https://github.com/43ravens/NEMO_Nowcast.git

if you don't have `ssh key authentication`_ set up on GitHub.

.. _ssh key authentication: https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh


.. _NEMO_NowcastDevelopmentEnvironment:

Development Environment
=======================

Setting up an isolated development environment using `Conda`_ is recommended.
Assuming that you have `Anaconda Python Distribution`_ or `Miniconda3`_ installed,
you can create and activate an environment called :kbd:`nemo-nowcast` that will have all of the Python packages necessary for development,
testing,
and building the documentation with the commands:

.. _Conda: http://conda.pydata.org/docs/
.. _Anaconda Python Distribution: https://www.continuum.io/downloads
.. _Miniconda3: http://conda.pydata.org/docs/install/quick.html

.. code-block:: bash

    $ cd  NEMO_Nowcast
    $ conda env create -f environment-dev.yaml
    $ source activate nemo-nowcast
    (nemo-nowcast)$ pip install --editable nemo_nowcast

The :kbd:`--editable` option in the :command:`pip install` command above installs the :kbd:`NEMO_Nowcast` package from the cloned repo via symlinks so that the installed :kbd:`nemo-nowcast` package will be automatically updated as the repo evolves.

To deactivate the environment use:

.. code-block:: bash

    (nemo-nowcast)$ source deactivate


.. _NEMO_NowcastCodingStyle:

Coding Style
============

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://black.readthedocs.io/en/stable/
    :alt: The uncompromising Python code formatter

The :kbd:`NEMO_Nowcast` package uses the `black`_ code formatting tool to maintain a coding style that is very close to `PEP 8`_.

.. _black: https://black.readthedocs.io/en/stable/
.. _PEP 8: https://www.python.org/dev/peps/pep-0008/

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

.. _reStructuredText: http://sphinx-doc.org/rest.html
.. _Sphinx: http://sphinx-doc.org/

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
whenever you push changes to GitHub the documentation is automatically re-built and rendered at http://nemo-nowcast.readthedocs.io/en/latest/.


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

    Removing everything under '_build'...
    Running Sphinx v5.3.0
    making output directory... done
    loading intersphinx inventory from https://docs.python.org/3/objects.inv...
    loading intersphinx inventory from https://gomss-nowcast-system.readthedocs.io/en/latest/objects.inv...
    loading intersphinx inventory from https://salishsea-nowcast.readthedocs.io/en/latest/objects.inv...
    building [mo]: targets for 0 po files that are out of date
    building [linkcheck]: targets for 18 source files that are out of date
    updating environment: [new config] 18 added, 0 changed, 0 removed
    reading sources... [100%] nowcast_system/workers
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [100%] nowcast_system/workers
    (           index: line   48) redirect  http://gomss-nowcast-system.readthedocs.io/en/latest/index.html - with Found to https://gomss-nowcast-system.readthedocs.io/en/latest/index.html
    (architecture/message_broker: line   48) redirect  http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html - with Found to https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html
    (     development: line  112) redirect  http://conda.pydata.org/docs/ - with Found to https://docs.conda.io/en/latest/
    (nowcast_system/workers: line  435) broken    http://crsmithdev.com/arrow/ - 404 Client Error: Not Found for url: https://crsmithdev.com/arrow/
    (nowcast_system/toy-example: line   32) broken    http://conda.pydata.org/docs/install/quick.html#linux-miniconda-install - 404 Client Error: Not Found for url: https://docs.conda.io/en/latest/install/quick.html
    (nowcast_system/toy-example: line  106) redirect  http://pyyaml.org/wiki/PyYAMLDocumentation - permanently to https://pyyaml.org/wiki/PyYAMLDocumentation
    (             api: line    3) redirect  http://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/index.html - with Found to https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/index.html
    (     development: line  228) redirect  http://nemo-nowcast.readthedocs.io/en/latest/ - with Found to https://nemo-nowcast.readthedocs.io/en/latest/
    (architecture/messaging: line  127) broken    http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLsyntax - Anchor 'YAMLsyntax' not found
    (         CHANGES: line   37) ok        http://supervisord.org/
    (     development: line  112) broken    http://conda.pydata.org/docs/install/quick.html - 404 Client Error: Not Found for url: https://docs.conda.io/en/latest/install/quick.html
    (     development: line  388) redirect  http://www.apache.org/licenses/LICENSE-2.0 - permanently to https://www.apache.org/licenses/LICENSE-2.0
    (architecture/message_broker: line   48) redirect  http://zeromq.org/ - permanently to https://zeromq.org/
    (     development: line  237) redirect  http://pytest.org/latest/ - with Found to https://pytest.org/en/7.2.x/
    (     development: line  184) redirect  http://sphinx-doc.org/ - with Found to https://www.sphinx-doc.org/en/master/
    (           index: line   21) redirect  http://www.nemo-ocean.eu/ - permanently to https://www.nemo-ocean.eu/
    (     development: line  184) redirect  http://sphinx-doc.org/rest.html - with Found to https://www.sphinx-doc.org/en/master/
    (     development: line  363) ok        https://anaconda.org/gomss-nowcast
    (     development: line   20) broken    https://anaconda.org/gomss-nowcast/nemo_nowcast/badges/installer/conda.svg - 404 Client Error: Not Found for url: https://anaconda.org/gomss-nowcast/nemo_nowcast/badges/installer/conda.svg
    (         CHANGES: line   68) redirect  https://api.slack.com/incoming-webhooks - with Found to https://api.slack.com/messaging/webhooks
    (nowcast_system/toy-example: line   40) ok        https://anaconda.org/GoMSS-Nowcast/nemo_nowcast
    (         CHANGES: line   65) broken    https://bitbucket.org/43ravens/nemo_nowcast/addon/pipelines/home - 404 Client Error: Not Found for url: https://bitbucket.org/43ravens/nemo_nowcast/addon/pipelines/home
    (         CHANGES: line   91) ok        https://black.readthedocs.io/en/stable/
    (nowcast_system/elements: line   24) broken    https://bitbucket.org/gomss-nowcast/gomss_nowcast - 404 Client Error: Not Found for url: https://bitbucket.org/gomss-nowcast/gomss_nowcast
    (         CHANGES: line   78) ok        https://calver.org/
    (     development: line  392) ok        https://boltons.readthedocs.io/en/latest/fileutils.html
    (     development: line   20) ok        https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg
    (         CHANGES: line  130) ok        https://boltons.readthedocs.io/en/latest/
    (     development: line   20) ok        https://docs.python.org/3.11/
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    (             api: line    3) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    (         CHANGES: line   37) ok        https://circus.readthedocs.io/en/latest/
    (         CHANGES: line   26) redirect  https://codecov.io/gh/43ravens/NEMO_Nowcast - permanently to https://app.codecov.io/gh/43ravens/NEMO_Nowcast
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.Namespace
    (             api: line    1) ok        https://docs.python.org/3/library/collections.html#collections.namedtuple
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#True
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#False
    (             api: line   22) ok        https://docs.python.org/3/library/constants.html#None
    (             api: line    1) ok        https://docs.python.org/3/library/functions.html#float
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    (             api: line    1) ok        https://docs.python.org/3/library/functions.html#int
    (             api: line    3) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    (             api: line    1) ok        https://docs.python.org/3/library/logging.html#logging.Logger
    (nowcast_system/elements: line   90) ok        https://docs.python.org/3/library/logging.html#logging.debug
    (nowcast_system/config: line   58) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.WatchedFileHandler
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.html#module-logging
    (     development: line   20) redirect  https://conda.anaconda.org/gomss-nowcast - with Found to https://anaconda.org/gomss-nowcast/repo?type=conda&label=main
    (     development: line  276) ok        https://coverage.readthedocs.io/en/latest/
    (             api: line    1) ok        https://docs.python.org/3/library/pathlib.html#pathlib.Path
    (             api: line    1) ok        https://docs.python.org/3/library/stdtypes.html#list
    (             api: line    1) ok        https://docs.python.org/3/library/stdtypes.html#bytes
    (             api: line    3) ok        https://docs.python.org/3/library/stdtypes.html#dict
    (             api: line    1) ok        https://docs.python.org/3/library/stdtypes.html#str
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/stdtypes.html#tuple
    (     development: line   70) ok        https://docs.python.org/3/reference/lexical_analysis.html#f-strings
    (     development: line   72) ok        https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep519
    (nowcast_system/elements: line   73) ok        https://docs.python.org/3/library/stdtypes.html#set
    (architecture/worker: line   29) ok        https://en.wikipedia.org/wiki/Idempotence
    (     development: line  335) ok        https://git-scm.com/
    (nowcast_system/toy-example: line  194) ok        https://en.wikipedia.org/wiki/INI_file
    (         CHANGES: line   30) ok        https://github.com/43ravens/NEMO_Nowcast
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg
    (         CHANGES: line   26) ok        https://github.com/43ravens/NEMO_Nowcast/actions
    (     development: line  310) ok        https://github.com/43ravens/NEMO_Nowcast/commits/main
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/issues
    (         CHANGES: line  184) ok        https://github.com/43ravens/NEMO_Nowcast/issues/2
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3ACI
    (         CHANGES: line  122) ok        https://github.com/43ravens/NEMO_Nowcast/issues/3
    (         CHANGES: line  197) ok        https://github.com/43ravens/NEMO_Nowcast/issues/4
    (         CHANGES: line  190) ok        https://github.com/43ravens/NEMO_Nowcast/issues/5
    (         CHANGES: line  144) ok        https://github.com/43ravens/NEMO_Nowcast/issues/7
    (     development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/CI/badge.svg
    (         CHANGES: line    8) ok        https://github.com/SalishSeaCast/SalishSeaCmd/actions?query=workflow%3Acodeql-analysis
    (         CHANGES: line  137) ok        https://github.com/43ravens/NEMO_Nowcast/issues/8
    (         CHANGES: line  105) ok        https://github.com/43ravens/NEMO_Nowcast/issues/9
    (     development: line  392) ok        https://github.com/mahmoud/boltons/blob/master/LICENSE
    (nowcast_system/workers: line  246) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (nowcast_system/workers: line   43) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#gomss-nowcastsystemworkers
    (     development: line   20) ok        https://img.shields.io/badge/code%20style-black-000000.svg
    (     development: line   20) ok        https://img.shields.io/badge/license-Apache%202-cb2533.svg
    (     development: line   20) ok        https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    (     development: line   20) ok        https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python&label=Python&logoColor=gold
    (     development: line   20) ok        https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    (     development: line   20) ok        https://nemo-nowcast.readthedocs.io/en/latest/
    (     development: line   20) ok        https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    (     development: line  321) redirect  https://help.github.com/en/actions - permanently to https://docs.github.com/en/actions
    (     development: line  102) redirect  https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh - permanently to https://docs.github.com/en/authentication/connecting-to-github-with-ssh
    (         CHANGES: line   60) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/elements.html#handling-worker-race-conditions
    (         CHANGES: line  111) ok        https://nemo-nowcast.readthedocs.io/en/latest/architecture/log_aggregator.html
    (     development: line   20) ok        https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    (     development: line   20) ok        https://opensource.org/licenses/BSD-3-Clause
    (     development: line  392) redirect  https://pypi.python.org/pypi/boltons - permanently to https://pypi.org/project/boltons/
    (           index: line   30) ok        https://salishsea-nowcast.readthedocs.io/en/latest/
    (     development: line  276) ok        https://pytest-cov.readthedocs.io/en/latest/
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadliveoceanworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makeliveoceanfilesworker
    (             api: line    3) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.next_workers
    (architecture/messaging: line   47) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.workers.download_weather
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#process-flow
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#nowcast.next_workers.after_collect_weather
    (nowcast_system/workers: line  354) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (nowcast_system/workers: line   44) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#salishseanowcastsystemworkers
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#gribtonetcdfworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#uploadforcingworker
    (nowcast_system/workers: line  322) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#watchnemo-worker
    (     development: line   20) ok        https://www.apache.org/licenses/LICENSE-2.0
    (         CHANGES: line   22) redirect  https://sentry.io - with Found to https://sentry.io/welcome/
    (     development: line   66) ok        https://www.python.org/
    (     development: line  147) redirect  https://www.python.org/dev/peps/pep-0008/ - with Found to https://peps.python.org/pep-0008/
    (     development: line  112) redirect  https://www.continuum.io/downloads - permanently to https://www.anaconda.com/products/distribution
    (           index: line   43) ok        https://salishsea.eos.ubc.ca/nemo/results/index.html
    build finished with problems, 4 warnings.

Look for any errors in the above output or in _build/linkcheck/output.txt

:command:`make linkcheck` is run monthly via a `scheduled GitHub Actions workflow`_

.. _scheduled GitHub Actions workflow: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck


.. _NEMO_NowcastRunningTheUnitTests:

Running the Unit Tests
======================

The test suite for the :kbd:`NEMO_Nowcast` package is in :file:`NEMO_Nowcast/tests/`.
The `pytest`_ tool is used for test parametrization and as the test runner for the suite.

.. _pytest: http://pytest.org/latest/

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

.. _GitHub Actions: https://help.github.com/en/actions


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


.. _NEMO_NowcastReleasePackages:

Release Packages
================

.. image:: https://anaconda.org/gomss-nowcast/nemo_nowcast/badges/installer/conda.svg
    :target: https://conda.anaconda.org/gomss-nowcast
    :alt: Install with conda

Versioned releases of the :kbd:`NEMO_Nowcast` package are available as `Conda`_ packages on `Anaconda.org`_.

.. _Anaconda.org: https://anaconda.org/gomss-nowcast

The latest release package can be installed with:

.. code-block:: bash

    $ conda install -c gomss-nowcast nemo_nowcast


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
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.

The `fileutils`_ module from the `boltons`_ project is included in the NEMO_Nowcast package.
It is copyright 2016 by Mahmoud Hashemi and used under the terms of the `boltons BSD license`_.

.. _fileutils: https://boltons.readthedocs.io/en/latest/fileutils.html
.. _boltons: https://pypi.python.org/pypi/boltons
.. _boltons BSD license: https://github.com/mahmoud/boltons/blob/master/LICENSE
