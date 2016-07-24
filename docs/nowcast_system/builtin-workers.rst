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


.. _BuiltinWorkers:

****************
Built-in Workers
****************

The framework provides a few worker modules for tasks that are generic enough that they are likely to be required in most nowcast systems.


.. _RotateLogsWorker:

:py:mod:`rotate_logs` Worker
============================

The :py:mod:`nemo_nowcast.workers.rotate_logs` worker iterates through the nowcast system logging handlers,
calling the :py:meth:`doRollover` method on any that are instances of
:py:class:`logging.handlers.RotatingFileHandler`.

Nowcast systems typically use rotating log files to avoid log files that grow without limit,
and to split the log information into logical pieces.
Please see :ref:`Logging` for more details of logging in nowcast systems,
and :ref:`LoggingConfig` for information about how to configure rotating log files.

Rotating the log files at the end of a day's nowcast processing is the recommended pattern.
To implement that in your nowcast system:

#. Add a :kbd:`rotate_logs` section to the :kbd:`workers` section of the :ref:`MessageRegistryConfig` section of your :ref:`NowcastConfigFile`:

   .. code-block:: yaml

       rotate_logs:
         checklist key: log rotation
         success: log files rotated
         failure: log file rotation failed
         crash: rotate_logs worker crashed

#. Add a :py:func:`after_rotate_logs` function to your :py:mod:`nowcast.next_workers` module:

   .. code-block:: python

       def after_rotate_logs(msg):
           """Calculate the list of workers to launch after the rotate_logs worker
           ends.

           :arg msg: Nowcast system message.
           :type msg: :py:class:`collections.namedtuple`

           :returns: Worker(s) to launch next
           :rtype: list
           """
           return []

   Since log file rotation is generally the last thing to happen in a nowcast's daily cycle of operations we simply return an empty list;
   i.e. there are no next workers.

#. Add a:

   .. code-block:: python

       NextWorker('nemo_nowcast.workers.rotate_logs')

   object to the list of next workers returned by the :py:func:`after_worker_name` function for the worker that you want the log file rotation operation to follow.


.. _ClearChecklistWorker:

:py:mod:`clear_checklist` Worker
================================

**TODO**:

* not yet implemented
