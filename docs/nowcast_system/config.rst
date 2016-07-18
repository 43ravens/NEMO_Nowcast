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


.. _NowcastConfigFile:

**************************
Nowcast Configuration File
**************************

**TODO**


.. _ZeroMQServerAndPortsConfig:

ZeroMQ Server and Ports
=======================

**TODO**

.. code-block:: yaml

    # Message system
    zmq:
      server: localhost
      ports:
        # traffic between manager and message broker
        manager: 4343
        # traffic between workers and message broker
        workers: 4344


.. _MessageRegistryConfig:

Message Registry
================

**TODO**
