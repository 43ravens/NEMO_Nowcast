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


.. _MessagingSystem:

****************
Messaging System
****************

Message Data Structure
======================

Inside the code of a worker and the nowcast manager,
a nowcast message is a Python object :py:class:`nemo_nowcast.message.Message`:

.. code-block:: python

    >>> from nemo_nowcast.message import Message

    >>> msg = Message(
            source='download_weather',
            type='success 12',
            payload={'12 forecast': True},
        )

The value associated with the :kbd:`source` attribute is the name of process that is sending the message;
i.e. the worker name,
or :kbd:`manager`.

.. code-block:: python

    >>> print(msg.source)
    'download_weather'

The :kbd:`type` attribute's value is a key associated with the message sender in the :ref:`MessageRegistryConfig` section of the :ref:`NowcastConfigFile`.
For example,
the message registry entries for a worker implemented in :py:mod:`~nowcast.workers.download_weather` might be:

.. code-block:: yaml

    message registry:
      ...
      workers:
        ...
        download_weather:
          ...
          success 00: 00 weather forecast ready
          failure 00: 00 weather forecast download failed
          success 06: 06 weather forecast ready
          failure 06: 06 weather forecast download failed
          success 12: 12 weather forecast ready
          failure 12: 12 weather forecast download failed
          success 18: 18 weather forecast ready
          failure 18: 18 weather forecast download failed
          crash: download_weather worker crashed
        ...

In the example message above:

.. code-block:: python

    >>> print(msg.type)
    'success 12'

The value associated with the :kbd:`payload` attribute can be any Python object
(including :py:obj:`None`)
that can be a value in a dictionary.
The payload value is inserted into a :kbd:`checklist` dictionary that the nowcast manager uses to maintain information about the state of the nowcast system.
The key at which the payload value is inserted into the checklist is defined for each worker in the :ref:`MessageRegistryConfig` section of the :ref:`NowcastConfigFile`:

.. code-block:: yaml

    message registry:
          ...
          workers:
            ...
            download_weather:
              checklist key: weather forecast
              ...

Message payloads vary markedly from one worker to another depending on what information a worker needs to convey to the manager,
other workers,
or nowcast system users inspecting the system state.


Message Exchanges
=================

Message exchanges are always initiated by workers.
Workers send a message to the manager when they have something significant to report:

* Successful completion of their task
* Failure to complete their task
* Crashing due to an unhandled exception
* Needing information from the manager about the state of the nowcast system
* Providing a message to be included in the nowcast system logging output
  (only from workers running on remote hosts)

When the manager receives a message from a worker it acknowledges the message with a return message.
Those messages are also defined in the :ref:`MessageRegistryConfig` section of the :ref:`NowcastConfigFile`.
An "all is good" acknowledgment message from the manager in response to a message from a worker looks like:

.. code-block:: python

    Message(
        source='manager',
        type='ack',
        payload=None,
    )


Message Serialization and Deserialization
=========================================

Before messages can be passed among a worker,
the :ref:`MessageBroker`,
and the :ref:`SystemManager` they must be transformed into strings for transmission across the network.
That is a process that is known as "serialization".
It is done by calling the :py:meth:`~nemo_nowcast.message.Message.serialize` method to transform the message object into a `YAML document`_:

.. _YAML document: http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLsyntax

.. code-block:: python

    Message(source='manager', type='ack').serialize()

The message recipient "deserializes" the YAML document to transform it back into a message :py:class:`~nemo_nowcast.message.Message`.
That is done by calling the :py:meth:`~nemo_nowcast.message.Message.deserialize` method with the YAML document as its argument:

.. code-block:: python

    message = Message.deserialize(yaml_string)

Deserialization is done using the :py:func:`yaml.safe_load()` function.
That function limits the types of Python objects that can be in a message to
(more or less)
the Python data
(:py:obj:`True`,
:py:obj:`False`,
:py:obj:`None`,
:py:obj:`float`,
:py:obj:`int`,
etc.)
and data container objects
(:py:obj:`dict`,
:py:obj:`list`,
:py:obj:`tuple`,
etc.).
Doing so is a security measure to prevent the possibility of injection into the system of a maliciously crafted message that could execute arbitrary code on the nowcast system server.


Network Transmission of Messages
================================

Messages are transmitted among the workers,
broker,
and the manager on the TCP network layer using dedicated ports.

* When the broker is started it binds to a workers port to listen for messages from workers,
  and a manager port to listen for messages from the manager.
  After that,
  the broker simply listens for messages and queues them in both directions between the workers and manager ports.
  It does not deserialize the YAML documents,
  it just passes them along.

* When the manager is started it connects to the manager port and listens for messages.
  When it receives a message it deserializes it,
  handles it,
  and send the appropriate acknowledgment message back.

* When a worker is started it connects to the workers port.
  When it has something to report to the manager it serializes the message,
  sends it,
  and waits for an acknowledgment from the manager.

The server on which the broker is running,
and the workers and manager port numbers that the system uses are defined in the :ref:`ZeroMQServerAndPortsConfig` section of the :ref:`NowcastConfigFile`.

.. note::
    If the manager or some of the workers run on different machines than the message broker it is necessary to ensure that the appropriate firewall rules are in place to allow traffic to pass between those machines via the worker and/or manager port(s).

The nowcast messaging system is based on the `ZeroMQ`_ distributed messaging framework.
You probably don't need to delve into the details of ZeroMQ,
but it is important to note that this is one of the situations where the nowcast system "stands on the shoulders of giants" rather than "re-inventing the wheel".

.. _ZeroMQ: http://zeromq.org/
