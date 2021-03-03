.. NEMO Nowcast Framework documentation master file

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

**********************************
NEMO Ocean Model Nowcast Framework
**********************************

The `NEMO_Nowcast`_ package is a collection of Python modules that can be used to build a software system to run the `NEMO ocean model`_ in a daily nowcast/forecast mode.
Such a system typically uses as-recent-as-available
forcing data or model products for open boundary conditions,
river run-off flows,
and atmospheric forcing.

.. _NEMO_Nowcast: https://github.com/43ravens/NEMO_Nowcast
.. _NEMO ocean model: http://www.nemo-ocean.eu/

The runs are automated using an asynchronous,
message-based architecture.
The `Salish Sea NEMO Nowcast system`_ is one example of a system built on this framework.
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

Documentation for the framework is in the ``docs/`` directory and is rendered at http://nemo-nowcast.readthedocs.io/en/latest/.


Contents
========

.. toctree::
   :maxdepth: 2

   architecture/index
   nowcast_system/index
   api
   development
   CHANGES


Indices
-------

* :ref:`genindex`
* :ref:`modindex`


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
