.. Copyright 2016 – present Doug Latornell, 43ravens

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

+----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Continuous Integration** | .. image:: https://github.com/43ravens/NEMO_Nowcast/actions/workflows/pytest-with-coverage.yaml/badge.svg                                                                                            |
|                            |      :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow:pytest-with-coverage                                                                                                   |
|                            |      :alt: Pytest with Coverage Status                                                                                                                                                               |
|                            | .. image:: https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg                                                                                                                   |
|                            |      :target: https://app.codecov.io/gh/43ravens/NEMO_Nowcast                                                                                                                                        |
|                            |      :alt: Codecov Testing Coverage Report                                                                                                                                                           |
|                            | .. image:: https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg                                                                                                 |
|                            |     :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow:CodeQL                                                                                                                  |
|                            |     :alt: CodeQL analysis                                                                                                                                                                            |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Documentation**          | .. image:: https://app.readthedocs.org/projects/nemo-nowcast/badge/?version=latest                                                                                                                   |
|                            |     :target: https://nemo-nowcast.readthedocs.io/en/latest/                                                                                                                                          |
|                            |     :alt: Documentation Status                                                                                                                                                                       |
|                            | .. image:: https://github.com/43ravens/NEMO_Nowcast/actions/workflows/sphinx-linkcheck.yaml/badge.svg                                                                                                |
|                            |     :target: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow:sphinx-linkcheck                                                                                                        |
|                            |     :alt: Sphinx linkcheck                                                                                                                                                                           |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Package**                | .. image:: https://img.shields.io/github/v/release/43ravens/NEMO_Nowcast?logo=github                                                                                                                 |
|                            |     :target: https://github.com/43ravens/NEMO_Nowcast/releases                                                                                                                                       |
|                            |     :alt: Releases                                                                                                                                                                                   |
|                            | .. image:: https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/43ravens/NEMO_Nowcast/main/pyproject.toml&logo=Python&logoColor=gold&label=Python      |
|                            |      :target: https://docs.python.org/3                                                                                                                                                              |
|                            |      :alt: Python Version from PEP 621 TOML                                                                                                                                                          |
|                            | .. image:: https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github                                                                                                                    |
|                            |     :target: https://github.com/43ravens/NEMO_Nowcast/issues                                                                                                                                         |
|                            |     :alt: Issue Tracker                                                                                                                                                                              |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Meta**                   | .. image:: https://img.shields.io/badge/license-Apache%202-cb2533.svg                                                                                                                                |
|                            |     :target: https://www.apache.org/licenses/LICENSE-2.0                                                                                                                                             |
|                            |     :alt: Licensed under the Apache License, Version 2.0                                                                                                                                             |
|                            | .. image:: https://img.shields.io/badge/License-BSD%203--Clause-orange.svg                                                                                                                           |
|                            |     :target: https://opensource.org/license/BSD-3-Clause                                                                                                                                             |
|                            |     :alt: Licensed under the BSD-3-Clause License                                                                                                                                                    |
|                            | .. image:: https://img.shields.io/badge/version%20control-git-blue.svg?logo=github                                                                                                                   |
|                            |     :target: https://github.com/43ravens/NEMO_Nowcast                                                                                                                                                |
|                            |     :alt: Git on GitHub                                                                                                                                                                              |
|                            +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                            | .. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json                                                                           |
|                            |     :target: https://pixi.prefix.dev/latest/                                                                                                                                                         |
|                            |     :alt: Pixi                                                                                                                                                                                       |
|                            | .. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white                                                                                              |
|                            |     :target: https://pre-commit.com                                                                                                                                                                  |
|                            |     :alt: pre-commit                                                                                                                                                                                 |
|                            | .. image:: https://img.shields.io/badge/code%20style-black-000000.svg                                                                                                                                |
|                            |     :target: https://black.readthedocs.io/en/stable/                                                                                                                                                 |
|                            |     :alt: The uncompromising Python code formatter                                                                                                                                                   |
|                            | .. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg                                                                                                                                |
|                            |     :target: https://github.com/pypa/hatch                                                                                                                                                           |
|                            |     :alt: Hatch project                                                                                                                                                                              |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. _NEMO_NowcastPythonVersions:

Python Versions
===============

.. image:: https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/43ravens/NEMO_Nowcast/main/pyproject.toml&logo=Python&logoColor=gold&label=Python
    :target: https://docs.python.org/3
    :alt: Python Version


The :py:obj:`NEMO_Nowcast` package is developed and tested using `Python`_ 3.14.
The minimum supported Python version is 3.12.
The :ref:`NEMO_NowcastContinuousIntegration` workflow on GitHub ensures that the package
is tested for all versions of Python>=3.12.

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

:py:obj:`NEMO_Nowcast` uses Pixi_ for package and environment management.
If you don't already have Pixi_ installed,
please follow its `installation instructions`_ to do so.

.. _Pixi: https://pixi.prefix.dev/latest/
.. _`installation instructions`: https://pixi.prefix.dev/latest/installation/

Install the development environment
(``dev``)
that includes the packages that :py:obj:`NEMO_Nowcast` depends on as well as various development tools packages with:

.. code-block:: bash

    $ cd NEMO_Nowcast
    $ pixi install --environment dev

Other environments used by commands in the sections below have addition packages for running
the test suite,
building and link checking the documentation,
etc.

If you are using an integrated development environment like VSCode or PyCharm
where you need a Python interpreter to support coding assistance features,
run development tasks,
etc.,
use the interpreter in the ``dev`` environment.
You can get its full path with :command:`pixi run -e dev which python`

To get detailed information about the environments,
the packages installed in them,
`Pixi`_ tasks that are defined for them,
etc.,
:use command:`pixi info`.

:py:obj:`NEMO_NowCast` is installed in `editable install mode`_ in all of the environments that
`Pixi`_ creates.
That means that changes you make to the code are immediately reflected in the environments.

.. _editable install mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs


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

To install the ``pre-commit`` hooks in a newly cloned repo run :command:`pre-commit install`:

.. code-block:: bash

    $ cd NEMO_Nowcast
    $ pixi run -e dev pre-commit install

.. note::
    You only need to install the hooks once immediately after you make a new clone of the
    `NEMO_Nowcast repository`_ and build your :ref:`NEMO_NowcastDevelopmentEnvironment`.

.. _NEMO_Nowcast repository: https://github.com/43ravens/NEMO_Nowcast


.. _NEMO_NowcastBuildingTheDocumentation:

Building the Documentation
==========================

.. image:: https://app.readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    :target: https://nemo-nowcast.readthedocs.io/en/latest/
    :alt: Documentation Status

The documentation for the :py:obj:`NEMO_Nowcast` package is written in `reStructuredText`_ and converted to HTML using `Sphinx`_.
Creating a :ref:`NEMO_NowcastDevelopmentEnvironment` as described above includes the installation of Sphinx.
Building the documentation is driven by the :file:`docs/Makefile`.
To do a clean build of the documentation use:

.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/

.. code-block:: bash

    $ cd NEMO_Nowcast
    $ pixi run docs

The output looks something like:

.. code-block:: text

    ✨ Pixi task (docs in docs): make clean html
    Removing everything under '_build'...
    Running Sphinx v8.1.3
    loading translations [en]... done
    making output directory... done
    loading intersphinx inventory 'python' from https://docs.python.org/3/objects.inv ...
    loading intersphinx inventory 'gomssnowcast' from https://gomss-nowcast-system.readthedocs.io/en/latest/objects.inv ...
    loading intersphinx inventory 'salishseanowcast' from https://salishsea-nowcast.readthedocs.io/en/latest/objects.inv ...
    building [mo]: targets for 0 po files that are out of date
    writing output...
    building [html]: targets for 18 source files that are out of date
    updating environment: [new config] 18 added, 0 changed, 0 removed
    reading sources... [100%] pkg_development
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    copying assets...
    copying static files...
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/language_data.js
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/documentation_options.js
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/basic.css
    Writing evaluated template result to /media/doug/warehouse/43ravens/projects/NEMO_Nowcast/docs/_build/html/_static/js/versions.js
    copying static files: done
    copying extra files...
    copying extra files: done
    copying assets: done
    writing output... [100%] pkg_development
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
Run the link checker with:

.. code-block:: bash

    $ cd NEMO_Nowcast
    $ pixi run linkcheck

The output looks something like:

.. code-block:: text

    ✨ Pixi task (linkcheck in docs): make clean linkcheck
    Removing everything under '_build'...
    Running Sphinx v8.1.3
    loading translations [en]... done
    making output directory... done
    loading intersphinx inventory 'python' from https://docs.python.org/3/objects.inv ...
    loading intersphinx inventory 'gomssnowcast' from https://gomss-nowcast-system.readthedocs.io/en/latest/objects.inv ...
    loading intersphinx inventory 'salishseanowcast' from https://salishsea-nowcast.readthedocs.io/en/latest/objects.inv ...
    building [mo]: targets for 0 po files that are out of date
    writing output...
    building [linkcheck]: targets for 18 source files that are out of date
    updating environment: [new config] 18 added, 0 changed, 0 removed
    reading sources... [100%] pkg_development
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    copying assets...
    copying assets: done
    writing output... [100%] pkg_development

    (nowcast_system/workers: line  439) ok        https://arrow.readthedocs.io/en/latest/
    (         CHANGES: line  129) ok        https://black.readthedocs.io/en/stable/
    (         CHANGES: line   64) ok        https://app.codecov.io/gh/43ravens/NEMO_Nowcast
    ( pkg_development: line   33) ok        https://app.readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    (nowcast_system/toy-example: line   40) ok        https://anaconda.org/GoMSS-Nowcast/nemo_nowcast
    (         CHANGES: line  168) ok        https://boltons.readthedocs.io/en/latest/
    (           index: line   91) ok        https://boltons.readthedocs.io/en/latest/fileutils.html
    (         CHANGES: line   75) ok        https://circus.readthedocs.io/en/latest/
    (         CHANGES: line   23) ok        https://coverage.readthedocs.io/en/latest/
    ( pkg_development: line   26) ok        https://codecov.io/gh/43ravens/NEMO_Nowcast/branch/main/graph/badge.svg
    (nowcast_system/toy-example: line   32) ok        https://docs.conda.io/en/latest/
    (         CHANGES: line  116) ok        https://calver.org/
    ( pkg_development: line   20) ok        https://docs.python.org/3
    (nowcast_system/toy-example: line   32) ok        https://docs.conda.io/en/latest/miniconda.html
    (             api: line    3) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    (             api: line   70) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    ( pkg_development: line  432) ok        https://docs.pytest.org/en/latest/
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.ArgumentTypeError
    (             api: line    1) ok        https://docs.python.org/3/library/argparse.html#argparse.Namespace
    (             api: line  124) ok        https://docs.python.org/3/library/collections.html#collections.namedtuple
    (             api: line   22) ok        https://docs.python.org/3/library/constants.html#None
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#False
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/constants.html#True
    (             api: line   61) ok        https://docs.python.org/3/library/functions.html#float
    (             api: line   61) ok        https://docs.python.org/3/library/functions.html#int
    (nowcast_system/config: line   58) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.WatchedFileHandler
    (             api: line    3) ok        https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    (architecture/manager: line   89) ok        https://docs.python.org/3/library/logging.html#logging.CRITICAL
    (             api: line   61) ok        https://docs.python.org/3/library/logging.html#logging.Logger
    (architecture/manager: line   53) ok        https://docs.python.org/3/library/logging.html#logging.ERROR
    (nowcast_system/config: line  138) ok        https://docs.python.org/3/library/logging.html#module-logging
    (nowcast_system/elements: line   90) ok        https://docs.python.org/3/library/logging.html#logging.debug
    (             api: line   25) ok        https://docs.python.org/3/library/pathlib.html#pathlib.Path
    (             api: line    3) ok        https://docs.python.org/3/library/stdtypes.html#dict
    (             api: line   61) ok        https://docs.python.org/3/library/stdtypes.html#bytes
    (             api: line  124) ok        https://docs.python.org/3/library/stdtypes.html#list
    (             api: line   34) ok        https://docs.python.org/3/library/stdtypes.html#str
    (nowcast_system/elements: line   73) ok        https://docs.python.org/3/library/stdtypes.html#set
    (architecture/messaging: line  146) ok        https://docs.python.org/3/library/stdtypes.html#tuple
    (architecture/worker: line   29) ok        https://en.wikipedia.org/wiki/Idempotence
    (nowcast_system/toy-example: line  194) ok        https://en.wikipedia.org/wiki/INI_file
    (         CHANGES: line  106) ok        https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/
    ( pkg_development: line  534) ok        https://git-scm.com/
    ( pkg_development: line  520) ok        https://docs.github.com/en/actions
    ( pkg_development: line   29) ok        https://github.com/43ravens/NEMO_Nowcast/actions/workflows/codeql-analysis.yaml/badge.svg
    ( pkg_development: line   23) ok        https://github.com/43ravens/NEMO_Nowcast/actions/workflows/pytest-with-coverage.yaml/badge.svg
    (         CHANGES: line   68) ok        https://github.com/43ravens/NEMO_Nowcast
    ( pkg_development: line   36) ok        https://github.com/43ravens/NEMO_Nowcast/actions/workflows/sphinx-linkcheck.yaml/badge.svg
    (         CHANGES: line   64) ok        https://github.com/43ravens/NEMO_Nowcast/actions
    ( pkg_development: line  500) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Apytest-with-coverage
    ( pkg_development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow:CodeQL
    ( pkg_development: line  260) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck
    ( pkg_development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow:pytest-with-coverage
    ( pkg_development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow:sphinx-linkcheck
    ( pkg_development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/issues
    ( pkg_development: line  509) ok        https://github.com/43ravens/NEMO_Nowcast/commits/main
    (         CHANGES: line  160) ok        https://github.com/43ravens/NEMO_Nowcast/issues/3
    (         CHANGES: line  235) ok        https://github.com/43ravens/NEMO_Nowcast/issues/4
    (         CHANGES: line  222) ok        https://github.com/43ravens/NEMO_Nowcast/issues/2
    (         CHANGES: line  228) ok        https://github.com/43ravens/NEMO_Nowcast/issues/5
    (         CHANGES: line  182) ok        https://github.com/43ravens/NEMO_Nowcast/issues/7
    ( pkg_development: line  502) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/pytest-with-coverage/badge.svg
    ( pkg_development: line  262) ok        https://github.com/43ravens/NEMO_Nowcast/workflows/sphinx-linkcheck/badge.svg
    (         CHANGES: line  175) ok        https://github.com/43ravens/NEMO_Nowcast/issues/8
    ( pkg_development: line   20) ok        https://github.com/43ravens/NEMO_Nowcast/releases
    -rate limited-   https://github.com/mahmoud/boltons/blob/master/LICENSE | sleeping...
    (           index: line   48) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/index.html
    (         CHANGES: line   41) ok        https://github.com/SalishSeaCast/SalishSeaCmd/actions?query=workflow%3Acodeql-analysis
    (nowcast_system/workers: line  245) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (nowcast_system/elements: line   24) ok        https://github.com/SalishSeaCast/SalishSeaNowcast
    (nowcast_system/workers: line   43) ok        https://gomss-nowcast-system.readthedocs.io/en/latest/workers.html#gomss-nowcastsystemworkers
    ( pkg_development: line   66) ok        https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
    ( pkg_development: line   53) ok        https://img.shields.io/badge/License-BSD%203--Clause-orange.svg
    ( pkg_development: line   20) ok        https://github.com/pypa/hatch
    (         CHANGES: line   24) ok        https://hatch.pypa.io/
    ( pkg_development: line   50) ok        https://img.shields.io/badge/license-Apache%202-cb2533.svg
    ( pkg_development: line   63) ok        https://img.shields.io/badge/code%20style-black-000000.svg
    ( pkg_development: line   56) ok        https://img.shields.io/badge/version%20control-git-blue.svg?logo=github
    ( pkg_development: line   60) ok        https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    ( pkg_development: line  561) ok        https://img.shields.io/badge/license-BSD%203--Clause-orange.svg
    ( pkg_development: line   43) ok        https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/43ravens/NEMO_Nowcast/main/pyproject.toml&logo=Python&logoColor=gold&label=Python
    (architecture/message_broker: line   48) ok        https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html
    ( pkg_development: line   40) ok        https://img.shields.io/github/v/release/43ravens/NEMO_Nowcast?logo=github
    (           index: line   59) ok        https://nemo-nowcast.readthedocs.io/en/latest/
    (         CHANGES: line  149) ok        https://nemo-nowcast.readthedocs.io/en/latest/architecture/log_aggregator.html
    ( pkg_development: line   46) ok        https://img.shields.io/github/issues/43ravens/NEMO_Nowcast?logo=github
    (             api: line    3) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/index.html
    (         CHANGES: line  143) ok        https://github.com/43ravens/NEMO_Nowcast/issues/9
    (         CHANGES: line   98) ok        https://nemo-nowcast.readthedocs.io/en/latest/nowcast_system/elements.html#handling-worker-race-conditions
    ( pkg_development: line  146) ok        https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    ( pkg_development: line   20) ok        https://opensource.org/license/BSD-3-Clause
    (           index: line   91) ok        https://pypi.org/project/boltons/
    ( pkg_development: line  112) ok        https://pixi.prefix.dev/latest/installation/
    ( pkg_development: line   20) ok        https://pre-commit.com
    ( pkg_development: line  165) ok        https://pre-commit.com/
    ( pkg_development: line  475) ok        https://pytest-cov.readthedocs.io/en/latest/
    ( pkg_development: line  112) ok        https://pixi.prefix.dev/latest/
    (architecture/messaging: line  127) ok        https://pyyaml.org/wiki/PyYAMLDocumentation
    (           index: line   30) ok        https://salishsea-nowcast.readthedocs.io/en/latest/
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadliveoceanworker
    (nowcast_system/workers: line  354) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#downloadweatherworker
    (nowcast_system/workers: line  336) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makesshfilesworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#gribtonetcdfworker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#makeliveoceanfilesworker
    (             api: line    3) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.next_workers
    (architecture/messaging: line   47) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#module-nowcast.workers.download_weather
    (nowcast_system/workers: line   44) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#salishseanowcastsystemworkers
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#process-flow
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#nowcast.next_workers.after_collect_weather
    (nowcast_system/workers: line  322) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#watchnemo-worker
    (nowcast_system/elements: line   67) ok        https://salishsea-nowcast.readthedocs.io/en/latest/workers.html#uploadforcingworker
    (         CHANGES: line   60) ok        https://sentry.io/welcome/
    (           index: line   43) ok        https://salishsea.eos.ubc.ca/nemo/results/index.html
    ( pkg_development: line   81) ok        https://www.python.org/
    (         CHANGES: line   75) ok        https://supervisord.org/
    ( pkg_development: line  195) ok        https://www.sphinx-doc.org/en/master/
    (           index: line   87) ok        https://www.apache.org/licenses/LICENSE-2.0
    ( pkg_development: line  195) ok        https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
    (architecture/message_broker: line   48) ok        https://zeromq.org/
    (           index: line   21) ok        https://www.nemo-ocean.eu/
    -rate limited-   https://github.com/mahmoud/boltons/blob/master/LICENSE | sleeping...
    -rate limited-   https://github.com/mahmoud/boltons/blob/master/LICENSE | sleeping...
    (           index: line   91) ok        https://github.com/mahmoud/boltons/blob/master/LICENSE
    build succeeded.

    Look for any errors in the above output or in _build/linkcheck/output.txt

:command:`pixi run linkcheck` is run monthly via a `scheduled GitHub Actions workflow`_

.. _scheduled GitHub Actions workflow: https://github.com/43ravens/NEMO_Nowcast/actions?query=workflow%3Asphinx-linkcheck


.. _NEMO_NowcastRunningTheUnitTests:

Running the Unit Tests
======================

The test suite for the :py:obj:`NEMO_Nowcast` package is in :file:`NEMO_Nowcast/tests/`.
The `pytest`_ tool is used for test parametrization and as the test runner for the suite.

.. _pytest: https://docs.pytest.org/en/latest/

Use:

.. code-block:: bash

    $ cd NEMO_Nowcast/
    $ pixi run pytest

to run the test suite.
The output looks something like:

.. code-block:: text

    ================================ test session starts =================================
    platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
    Using --randomly-seed=2471750703
    rootdir: /media/doug/warehouse/43ravens/projects/NEMO_Nowcast
    configfile: pyproject.toml
    plugins: cov-7.0.0, randomly-3.15.0
    collected 319 items

    tests/test_manager.py ................................................................
    ...................                                                             [ 26%]
    tests/workers/test_rotate_logs.py .................                             [ 31%]
    tests/test_message_broker.py ...................                                [ 37%]
    tests/workers/test_clear_checklist.py .........                                 [ 40%]
    tests/test_log_aggregator.py .................                                  [ 45%]
    tests/test_scheduler.py ...................                                     [ 51%]
    tests/test_cli.py .................                                             [ 56%]
    tests/workers/test_sleep.py .........                                           [ 59%]
    tests/test_next_workers.py ......                                               [ 61%]
    tests/test_worker.py .................................................................
    ...........................                                                     [ 90%]
    tests/test_message.py ......                                                    [ 92%]
    tests/workers/test_awaken.py ........                                           [ 94%]
    tests/test_config.py .................                                          [100%]

    ================================ 319 passed in 18.66s ================================

You can monitor what lines of code the test suite exercises using the `coverage.py`_ and `pytest-cov`_ tools with the commands:

.. _coverage.py: https://coverage.readthedocs.io/en/latest/
.. _pytest-cov: https://pytest-cov.readthedocs.io/en/latest/

.. code-block:: bash

    $ cd NEMO_Nowcast/
    $ pixi run pytest-cov

The test coverage report will be displayed below the test suite run output.

Alternatively,
you can use

.. code-block:: bash

    $ pixi run pytest-cov-html

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

The NEMO_Nowcast framework code and documentation are copyright 2016 – present by Doug Latornell, 43ravens.

They are licensed under the Apache License, Version 2.0.
https://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.

The `fileutils`_ module from the `boltons`_ project is included in the NEMO_Nowcast package.
It is copyright 2016 by Mahmoud Hashemi and used under the terms of the `boltons BSD license`_.

.. _fileutils: https://boltons.readthedocs.io/en/latest/fileutils.html
.. _boltons: https://pypi.org/project/boltons/
.. _boltons BSD license: https://github.com/mahmoud/boltons/blob/master/LICENSE


Release Process
===============

.. image:: https://img.shields.io/github/v/release/43ravens/NEMO_Nowcast?logo=github
    :target: https://github.com/43ravens/NEMO_Nowcast/releases
    :alt: Releases
.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
    :target: https://github.com/pypa/hatch
    :alt: Hatch project

Releases are done at Doug's discretion when significant pieces of development work have been
completed.

The release process steps are:

#. Use :command:`hatch version release` to bump the version from ``.devn`` to the next release
   version identifier

#. Edit :file:`docs/CHANGES.rst` to update the version identifier and replace ``unreleased``
   with the release date

#. Commit the version bump and change log update

#. Create and annotated tag for the release with :guilabel:`Git -> New Tag...` in PyCharm
   or :command:`git tag -e -a vyy.n`

#. Push the version bump commit and tag to GitHub

#. Use the GitHub web interface to create a release,
   editing the auto-generated release notes into sections:

   * Features
   * Bug Fixes
   * Documentation
   * Maintenance
   * Dependency Updates

#. Use the GitHub :guilabel:`Issues -> Milestones` web interface to edit the release
   milestone:

   * Change the :guilabel:`Due date` to the release date
   * Delete the "when it's ready" comment in the :guilabel:`Description`

#. Use the GitHub :guilabel:`Issues -> Milestones` web interface to create a milestone for
   the next release:

   * Set the :guilabel:`Title` to the next release version,
     prepended with a ``v``;
     e.g. ``v25.1``
   * Set the :guilabel:`Due date` to the end of the year of the next release
   * Set the :guilabel:`Description` to something like
     ``v25.1 release - when it's ready :-)``
   * Create the next release milestone

#. Review the open issues,
   especially any that are associated with the milestone for the just released version,
   and update their milestone.

#. Close the milestone for the just released version.

#. Use :command:`hatch version minor,dev` to bump the version for the next development cycle,
   or use :command:`hatch version major,minor,dev` for a year rollover version bump

#. Edit :file:`docs/CHANGES.rst` to add a new section for the unreleased dev version

#. Commit the version bump and change log update

#. Push the version bump commit to GitHub
