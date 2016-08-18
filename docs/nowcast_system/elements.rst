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


.. _ElementsOfANowcastSystem:

****************************
Elements of a Nowcast System
****************************

**TODO**:

* Python package; e.g. `GoMSS_Nowcast`_

  .. _GoMSS_Nowcast: https://bitbucket.org/gomss-nowcast/gomss_nowcast

* version control is highly recommended
* nowcast system configuration
* workers
* next_workers module
* process management with circus
* distribute releases via an anaconda.org channel or conda-forge


.. _Logging:

Logging
=======

**TODO**:

* logging levels and readability of log files
* log file rotation and growth limitation
* environment variable substitution in logging config
* serve log files on web page if possible, or use log aggregation service
* exception logging to Sentry
* machine readable logging; JSON via Driftwood


.. _NextWorkersModule:

Next Workers Module
===================

**TODO**
