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

This worker is normally launched in automation at the end of a nowcast processing cycle (e.g. end of the day).

It can also be launched from the command-line by the nowcast administrator as necessary for system maintenance.

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

       def after_rotate_logs(msg, config, checklist):
           """Calculate the list of workers to launch after the rotate_logs worker
           ends.

           :arg msg: Nowcast system message.
           :type msg: :py:class:`collections.namedtuple`

           :arg config: :py:class:`dict`-like object that holds the nowcast system
                        configuration that is loaded from the system configuration
                        file.
           :type config: :py:class:`nemo_nowcast.config.Config`

           :arg dict checklist: System checklist: data structure containing the
                                present state of the nowcast system.

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

   The recommended pattern is that the :py:mod:`rotate_logs` worker be launched immediately after successful execution of the :ref:`ClearChecklistWorker`.


.. _ClearChecklistWorker:

:py:mod:`clear_checklist` Worker
================================

The :py:mod:`nemo_nowcast.workers.clear_checklist` worker sends a message to the nowcast system manager requesting that it clear its system state checklist.

This worker is normally launched in automation at the end of a nowcast processing cycle
(e.g. end of the day),
just prior to launching the :ref:`RotateLogsWorker`.

It can also be launched from the command-line by the nowcast administrator as necessary for system maintenance.

Clearing the checklist just before rotating the log files at the end of a day's nowcast processing is the recommended pattern.
To implement that in your nowcast system:

#. Add a :py:mod:`clear_checklist` section to the :kbd:`workers` section of the :ref:`MessageRegistryConfig` section of your :ref:`NowcastConfigFile`:

   .. code-block:: yaml

       clear_checklist:
         clear checklist: request that manager clear system state checklist
         success: system state checklist cleared
         failure: system state checklist clearance failed
         crash: clear_checklist worker crashed

   .. note::
      No :kbd:`checklist key` element is required because the :kbd:`clear_checklist` worker is a special case worker that does not return any information to add to the checklist
      (having just requested that it be cleared).

#. Add a :py:func:`after_clear_checklist` function to your :py:mod:`nowcast.next_workers` module:

   .. code-block:: python

       def after_clear_checklist(msg, config, checklist):
           """Calculate the list of workers to launch after the clear_checklist worker
           ends.

           :arg msg: Nowcast system message.
           :type msg: :py:class:`collections.namedtuple`

           :arg config: :py:class:`dict`-like object that holds the nowcast system
                        configuration that is loaded from the system configuration
                        file.
           :type config: :py:class:`nemo_nowcast.config.Config`

           :arg dict checklist: System checklist: data structure containing the
                                present state of the nowcast system.

           :returns: Worker(s) to launch next
           :rtype: list
           """
           next_workers = {
               'crash': [],
               'failure': [],
               'success': [NextWorker('nemo_nowcast.workers.rotate_logs')],
           }
           return next_workers[msg.type]

   The recommended pattern is to launch the :ref:`RotateLogsWorker` upon success of the :py:mod:`clear_checklist` worker.

#. Add a:

   .. code-block:: python

       NextWorker('nemo_nowcast.workers.clear_checklist')

   object to the list of next workers returned by the :py:func:`after_worker_name` function for the worker that you want the log file rotation operation to follow.
