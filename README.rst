**********************************
NEMO Ocean Model Nowcast Framework
**********************************

The `NEMO_Nowcast`_ package is a collection of Python modules that can be used to build a software system to run the `NEMO ocean model`_ in a daily nowcast/forecast mode.
Such a system typically uses as-recent-as-available
forcing data or model products for open boundary conditions,
river run-off flows,
and atmospheric forcing.

.. _NEMO_Nowcast: https://anaconda.org/GoMSS-Nowcast/nemo_nowcast
.. _NEMO ocean model: http://www.nemo-ocean.eu/

The runs are automated using an asynchronous,
message-based architecture.
The `Salish Sea NEMO Nowcast system`_ is an example of a system built on this framework.
That system:

* obtains the forcing datasets from web services
* pre-processes the forcing datasets into the formats expected by NEMO
* uploads the forcing dataset files to the HPC or cloud-computing facility where the run will be executed
* executes the run
* downloads the results
* prepares a collection of plots from the run results for monitoring purposes
* publishes the plots and the processing log to the web

to produce a `daily nowcast and 2 forecasts`_ of the state of the Salish Sea on the west coast of British Columbia.

.. _Salish Sea NEMO Nowcast system: https://salishsea-nowcast.readthedocs.io/en/latest/
.. _daily nowcast and 2 forecasts: https://salishsea.eos.ubc.ca/nemo/results/index.html

The `GoMSS Nowcast System`_ is another example of a system built on this framework.
It:

* obtains the forcing and opern boundary conditions datasets from web services
* pre-processes the forcing datasets into the formats expected by NEMO
* executes the run

to produce daily nowcast runs that calculate the state of the Gulf of Maine and the Scotian Shelf on the east coast of Nova Scotia.

.. _GoMSS Nowcast System: http://gomss-nowcast-system.readthedocs.io/en/latest/index.html


Documentation
=============

Documentation for the framework is in the ``docs/`` directory and is rendered at http://nemo-nowcast.readthedocs.io/en/latest/.

.. image:: https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    :target: http://nemo-nowcast.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Build Status


Release Packages
================

In addition to the `NEMO_Nowcast`_ code repository,
release packages are available from the `gomss-nowcast channel`_ at anaconda.org.

.. _gomss-nowcast channel: https://anaconda.org/GoMSS-Nowcast/repo

.. image:: https://anaconda.org/gomss-nowcast/nemo_nowcast/badges/installer/conda.svg
    :target: https://conda.anaconda.org/gomss-nowcast/repo
    :alt: Install with Conda

.. image:: https://anaconda.org/gomss-nowcast/nemo_nowcast/badges/downloads.svg
    :target: https://anaconda.org/GoMSS-Nowcast/nemo_nowcast
    :alt: Install latest release



Licenses
========

The NEMO_Nowcast framework code and documentation are copyright 2016 by Doug Latornell, 43ravens.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.

The `fileutils`_ module from the `boltons`_ project is included in the NEMO_Nowcast package.
It is copyright 2013-2016 by Mahmoud Hashemi and used under the terms of the `boltons BSD license`_.

.. _fileutils: https://boltons.readthedocs.io/en/latest/fileutils.html
.. _boltons: https://pypi.python.org/pypi/boltons
.. _boltons BSD license: https://github.com/mahmoud/boltons/blob/master/LICENSE
