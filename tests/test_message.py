# Copyright 2016 – present Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for message module."""

import pytest
import yaml

from nemo_nowcast import Message


class TestMessage:
    """Unit tests for nemo_nowcast.message.Message class."""

    def test_default_attrs(self):
        msg = Message("test_runner", "foo")
        assert msg.source == "test_runner"
        assert msg.type == "foo"
        assert msg.payload is None

    def test_payload_attr(self):
        msg = Message("test_runner", "foo", "payload")
        assert msg.source == "test_runner"
        assert msg.type == "foo"
        assert msg.payload == "payload"

    @pytest.mark.parametrize(
        "source, msg_type, payload",
        [
            ("manager", "unregistered worker", None),
            ("download_weather", "success 00", {"00 forecast": True}),
        ],
    )
    def test_serialize(self, source, msg_type, payload):
        msg = Message(source, msg_type, payload).serialize()
        expected = {"source": source, "type": msg_type, "payload": payload}
        assert yaml.safe_load(msg) == expected

    @pytest.mark.parametrize(
        "source, msg_type, payload",
        [
            ("manager", "ack", None),
            ("download_weather", "success 00", {"00 forecast": True}),
        ],
    )
    def test_deserialize(self, source, msg_type, payload):
        message = yaml.dump({"source": source, "type": msg_type, "payload": payload})
        msg = Message.deserialize(message)
        assert msg.source == source
        assert msg.type == msg_type
        assert msg.payload == payload
