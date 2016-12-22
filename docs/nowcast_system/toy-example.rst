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

***********************************
A "Toy" Example of a Nowcast System
***********************************

In the spirit of "learn by doing",
this section presents the practical details of building and operating a nowcast system by setting up a "toy" nowcast system with a few trival :ref:`ExampleWorkers`.
The :ref:`subsequent sections <BuildingANowcastSystem>` provide more details reference documentation building and operating software automation systems based on this framework.


Conda Environment
=================

We'll use a `Conda`_ environment to isolate Python package installation.
`Miniconda3`_ provides the :command:`conda` package manager and environment management tools.
Please follow the `Linux Miniconda Install`_ instructions to download and install Miniconda.

.. _Conda: http://conda.pydata.org/docs/
.. _Miniconda3: http://conda.pydata.org/docs/install/quick.html
.. _Linux Miniconda Install: http://conda.pydata.org/docs/install/quick.html#linux-miniconda-install

Once that is done,
create a conda environment with the `NEMO_Nowcast`_ package and its dependencies installed in it with the command:

.. _NEMO_Nowcast: https://anaconda.org/GoMSS-Nowcast/nemo_nowcast

.. code-block:: bash

    $ conda create -n toy-nowcast -c gomss-nowcast nemo_nowcast

Activate the environment with:

.. code-block:: bash

    $ source activate toy-nowcast

To deactivate the environment later,
use:

.. code-block:: bash

    (toy-nowcast)$ source deactivate toy-nowcast


**TODO**:

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
