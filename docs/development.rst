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


.. _NEMO_NowcastPackageDevelopment:

***************************************
:kbd:`NEMO_Nowcast` Package Development
***************************************

.. _NEMO_NowcastPythonVersions:

Python Versions
===============

The :kbd:`NEMO_Nowcast` package is developed and tested using `Python`_ 3.5 or later.

.. _Python: https://www.python.org/


.. _NEMO_NowcastGettingTheCode:

Getting the Code
================

Clone the code and documentation `repository`_ from Bitbucket with:

.. _repository: https://bitbucket.org/43ravens/nemo_nowcast

.. code-block:: bash

    $ hg clone ssh://hg@bitbucket.org/43ravens/nemo_nowcast NEMO_Nowcast

or

.. code-block:: bash

    $ hg clone https://your_userid@bitbucket.org/43ravens/nemo_nowcast NEMO_Nowcast

if you don't have `ssh key authentication`_ set up on Bitbucket.

.. _ssh key authentication: https://confluence.atlassian.com/bitbucket/set-up-ssh-for-mercurial-728138122.html


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


.. _NEMO_NowcastBuildingTheDocumentation:

Building the Documentation
==========================

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
The output looks something like::

  rm -rf _build/*
  sphinx-build -b html -d _build/doctrees   . _build/html
  Running Sphinx v1.4.1
  making output directory...
  loading pickled environment... not yet created
  loading intersphinx inventory from https://docs.python.org/objects.inv...
  building [mo]: targets for 0 po files that are out of date
  building [html]: targets for 2 source files that are out of date
  updating environment: 2 added, 0 changed, 0 removed
  reading sources... [100%] index
  looking for now-outdated files... none found
  pickling environment... done
  checking consistency... done
  preparing documents... done
  writing output... [100%] index
  generating indices... genindex
  writing additional pages... search
  copying static files... done
  copying extra files... done
  dumping search index in English (code: en) ... done
  dumping object inventory... done
  build succeeded.

  Build finished. The HTML pages are in _build/html.

The HTML rendering of the docs ends up in :file:`docs/_build/html/`.
You can open the :file:`index.html` file in that directory tree in your browser to preview the results of the build.

If you have write access to the `repository`_ on Bitbucket,
whenever you push changes to Bitbucket the documentation is automatically re-built and rendered at http://nemo-nowcast.readthedocs.io/en/latest/.


.. _NEMO_NowcastRuningTheUnitTests:

Running the Unit Tests
======================

The test suite for the :kbd:`NEMO_Nowcast` package is in :file:`NEMO_Nowcast/tests/`.
The `pytest`_ tool is used for test parametrization and as the test runner for the suite.

.. _pytest: http://pytest.org/latest/

With your :kbd:`nemo-nowcast` development environment activated,
use:

.. _Mercurial: https://www.mercurial-scm.org/

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/
    (nemo-nowcast)$ py.test

to run the test suite.
The output looks something like::

  ============================ test session starts ============================
  platform linux -- Python 3.5.1, pytest-2.8.1, py-1.4.31, pluggy-0.3.1
  rootdir: /home/doug/Documents/43ravens/projects/gomss-nowcast/NEMO_Nowcast, inifile:
  collected 8 items

  tests/test_lib.py ........

  ========================= 8 passed in 0.09 seconds ==========================

You can monitor what lines of code the test suite exercises using the `coverage.py`_ tool with the command:

.. _coverage.py: https://coverage.readthedocs.io/en/latest/

.. code-block:: bash

    (nemo-nowcast)$ cd NEMO_Nowcast/
    (nemo-nowcast)$ coverage run -m py.test

and generate a test coverage report with:

.. code-block:: bash

    (nemo-nowcast)$ coverage report

to produce a plain text report,
or

.. code-block:: bash

    (nemo-nowcast)$ coverage html

to produce an HTML report that you can view in your browser by opening :file:`NEMO_Nowcast/htmlcov/index.html`.


.. _NEMO_NowcastVersionControlRepository:

Version Control Repository
==========================

The :kbd:`NEMO_Nowcast` package code and documentation source files are available as a `Mercurial`_ repository at https://bitbucket.org/43ravens/nemo_nowcast.


.. _NEMO_NowcastIssueTracker:

Issue Tracker
=============

Development tasks,
bug reports,
and enhancement ideas are recorded and managed in the issue tracker at https://bitbucket.org/43ravens/nemo_nowcast/issues.


.. _NEMO_NowcastReleasePackages:

Release Packages
================

Versioned releases of the :kbd:`NEMO_Nowcast` package are available as `Conda`_ packages on `Anaconda.org`_.

.. _Anaconda.org: https://anaconda.org/gomss-nowcast

The latest release package can be installed with:

.. code-block:: bash

    $ conda install -c gomss-nowcast nemo_nowcast
