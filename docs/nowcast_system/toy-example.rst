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


.. _ToyExample:

************************************
A "Toy" Example of a  Nowcast System
************************************

**TODO**:

* create a conda environment, installing all dependencies via default and gomss-nowcast channels
* create a :file:`nowcast/` directory
* create :file:`nowcast/nowcast.yaml` like :file:`example_nowcast.yaml`
* create :file:`nowcast/circus.ini` like :file:`example_circus.ini`
* create :file:`nowcast/next_workers.py`
* run :command:`circusd circus.ini` in one terminal session
* run :command:`python -m nemo_nowcast.workers.sleep nowcast.yaml` in a 2nd terminal session

* exercises:

  * experiment with running sleep worker with :kbd:`--sleep-time` and/or :kbd:`--debug`
    command-line flags
  * run :command:`circusctl` in a 3rd terminal session
  * :command:`status`
  * change zmq workers port in :file:`nowcast.yaml`,
    use :command:`signal manager hup` to reload manager config,
    run sleep worker again
  * add :py:func:`after_rotate_logs` function to :py:mod:`next_workers` module
  * run :command:`python -m nemo_nowcast.workers.rotate_logs nowcast.yaml`
  * add rotate_logs worker to after_awaken function,
    run sleep worker again
