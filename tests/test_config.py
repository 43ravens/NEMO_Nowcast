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

"""Unit tests for config module."""

from unittest.mock import Mock, mock_open, patch

import pytest

from nemo_nowcast.config import Config


class TestConfig:
    """Unit tests for nemo_nowcast.config.Config class."""

    def test_default_attrs(self):
        config = Config()
        assert config.file == ""
        assert config._dict == {}

    def test_keyerror(self):
        config = Config()
        with pytest.raises(KeyError):
            config["foo"]

    def test_contains(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert "foo" in config

    def test_getitem(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config["foo"] == "bar"

    def test_setitem(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        config["foo"] = "baz"
        assert config["foo"] == "baz"

    def test_set_key_exists(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config.get("foo") == "bar"

    def test_set_no_key_default_none(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config.get("bar") is None

    def test_set_no_key_default_value(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config.get("bar", default="baz") == "baz"


class TestConfigLoad:
    """Unit tests for nemo_nowcast.config.Config.load method."""

    def test_file_attr_set(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config.file == "nowcast.yaml"

    def test_load(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config["foo"] == "bar"

    def test_replace_checklist_file_envvar(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: $(NOWCAST.ENV.foo)/nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        config._replace_env = Mock(return_value="bar")
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config["checklist file"] == "bar/nowcast_checklist.yaml"

    def test_replace_python_interpreter_envvar(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: $(NOWCAST.ENV.foo)/bin/python\n"
                "logging:\n"
                "  handlers: []"
            )
        )
        config = Config()
        config._replace_env = Mock(return_value="bar")
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config["python"] == "bar/bin/python"

    def test_replace_log_file_envvar_local_logging(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers:\n"
                "    info_test:\n"
                "      filename: $(NOWCAST.ENV.foo)/nowcast.log"
            )
        )
        config = Config()
        config._replace_env = Mock(return_value="bar")
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        filename = config["logging"]["handlers"]["info_test"]["filename"]
        assert filename == "bar/nowcast.log"

    def test_replace_log_file_envvar_distributed_logging(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  aggregator:\n"
                "    handlers:\n"
                "      info_test:\n"
                "        filename: $(NOWCAST.ENV.foo)/nowcast.log\n"
                "  publisher:\n"
                "    handlers:\n"
                "      wgrib2_test:\n"
                "        filename: $(NOWCAST.ENV.foo)/wgrib2.log"
            )
        )
        config = Config()
        config._replace_env = Mock(return_value="bar")
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        filename = config["logging"]["aggregator"]["handlers"]["info_test"]["filename"]
        assert filename == "bar/nowcast.log"
        filename = config["logging"]["publisher"]["handlers"]["wgrib2_test"]["filename"]
        assert filename == "bar/wgrib2.log"

    def test_ignore_log_stream_handler(self):
        m_open = mock_open(
            read_data=(
                "foo: bar\n"
                "checklist file: nowcast_checklist.yaml\n"
                "python: python\n"
                "logging:\n"
                "  handlers:\n"
                "    console: {}"
            )
        )
        config = Config()
        config._replace_env = Mock(return_value="bar")
        with patch("nemo_nowcast.config.open", m_open):
            config.load("nowcast.yaml")
        assert config._replace_env.call_count == 0


class TestReplaceEnv:
    """Unit tests for nemo_nowcast.config.Config._replace_env load method."""

    @patch.dict("nemo_nowcast.config.os.environ", {"foo": "bar"})
    def test_replace_env(self):
        var = Mock(name="re_var", group=Mock(return_value="foo"))
        value = Config._replace_env(var)
        assert value == "bar"

    def test_envvar_not_set(self):
        var = Mock(name="re_var", group=Mock(return_value="foo"))
        with pytest.raises(KeyError):
            value = Config._replace_env(var)
