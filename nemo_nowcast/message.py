# Copyright 2016-2021 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast framework message object.
"""
import attr
import yaml


@attr.s
class Message:
    """Construct a :py:class:`nemo_nowcast.message.Message` instance.
    """

    #: Name of the worker or manager sending the message.
    source = attr.ib()
    #: Key of a message type that is defined for source in the message
    #: registry section of the configuration data structure.
    type = attr.ib()
    #: Content of message; must be serializable by YAML such that it can be
    #: deserialized by :py:func:`yaml.safe_load`.
    payload = attr.ib(default=None)

    def serialize(self):
        """Construct a message data structure and transform it into a string
        suitable for sending.

        :returns: Message data structure serialized using YAML.
        """
        return yaml.dump(
            {"source": self.source, "type": self.type, "payload": self.payload}
        )

    @classmethod
    def deserialize(cls, message):
        """Transform received message from str to message data structure.

        :arg str message: Message dict serialized using YAML.

        :returns: :py:class:`nemo_nowcast.lib.Message` instance
        """
        msg = yaml.safe_load(message)
        return cls(source=msg["source"], type=msg["type"], payload=msg["payload"])
