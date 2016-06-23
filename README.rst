**********************************
NEMO Ocean Model Nowcast Framework
**********************************

The `NEMO_Nowcast`_ package is a collection of Python modules that can be used to build a software system to run the NEMO ocean model in a daily nowcast/forecast mode.
Such a system typically uses as-recent-as-available
forcing data or model products for open boundary conditions,
river run-off flows,
and atmospheric forcing.

.. _NEMO_Nowcast: https://anaconda.org/GoMSS-Nowcast/nemo_nowcast

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

.. _Salish Sea NEMO Nowcast system: http://salishsea-meopar-tools.readthedocs.io/en/latest/SalishSeaNowcast/
.. _daily nowcast and 2 forecasts: https://salishsea.eos.ubc.ca/nemo/results/index.html

Documentation for the framework is in the ``docs/`` directory and is rendered at http://nemo-nowcast.readthedocs.io/en/latest/.

.. image:: https://readthedocs.org/projects/nemo-nowcast/badge/?version=latest
    :target: http://nemo-nowcast.readthedocs.io/en/latest/?badge=latest
    :title: Documentation Build Status
    :alt: Documentation Build Status

License
=======

The NEMO_Nowcast framework code and documentation are copyright 2016 by Doug Latornell, 43ravens.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
