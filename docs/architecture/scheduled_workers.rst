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


.. _ScheduledWorkers:

*****************
Scheduled Workers
*****************

**TODO**:

* feature not yet implemented
* separate process process under circusd that launches worker(s) as scheduled time(s)
* intended for use for tasks that depend on timing that is controlled outside the  nowcast system;
  primary example is download_weather worker that needs to start at a time after the weather model product files become available (on, for example, the EC FTP server)
