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

"""NEMO_Nowcast framework system configuration object.

Provides :py:class:`dict`-like access to the configuration loaded from the
YAML system configuration file.
"""
import os
import re

import attr
import yaml


@attr.s
class Config:
    """Construct a :py:class:`nemo_nowcast.config.Config` instance."""

    #: Path/name of YAML configuration file for the NEMO nowcast system.
    #: Assigned when :py:meth:`~nemo_nowcast.config.Config.load` method
    #: is called.
    file = attr.ib(init=False, default="")
    #: :py:class:`dict` containing the nowcast system configuration
    #: that is read from the configuration file by the
    #: :py:meth:`~nemo_nowcast.config.Config.load` method.
    _dict = attr.ib(init=False, repr=False, default=attr.Factory(dict))

    def __contains__(self, item):
        return item in self._dict

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def get(self, key, default=None):
        try:
            return self._dict[key]
        except KeyError:
            return default

    def load(self, config_file):
        """Load the YAML config_file.

        The value of config_file is stored on the
        :py:attr:`nemo_nowcast.config.Config.file` attribute.

        :arg config_file: Path/name of YAML configuration file for the NEMO nowcast system.
        :type config_file: :py:class:`pathlib.Path` or str
        """
        self.file = config_file
        with open(config_file, "rt") as f:
            self._dict = yaml.safe_load(f)
        envvar_pattern = re.compile(r"\$\(NOWCAST\.ENV\.(\w*)\)\w*")
        envvar_sub_keys = ("checklist file", "python")
        for key in envvar_sub_keys:
            self._dict[key] = envvar_pattern.sub(self._replace_env, self._dict[key])

        try:
            # Local logging
            self._replace_handler_envvars(
                envvar_pattern, self._dict["logging"]["handlers"]
            )
        except KeyError:
            # Distributed logging
            self._replace_handler_envvars(
                envvar_pattern, self._dict["logging"]["aggregator"]["handlers"]
            )
            self._replace_handler_envvars(
                envvar_pattern, self._dict["logging"]["publisher"]["handlers"]
            )

    def _replace_handler_envvars(self, envvar_pattern, handlers):
        for handler in handlers:
            try:
                handlers[handler]["filename"] = envvar_pattern.sub(
                    self._replace_env, handlers[handler]["filename"]
                )
            except KeyError:
                # Not a file handler
                pass

    @staticmethod
    def _replace_env(var):
        try:
            return os.environ[var.group(1)]
        except KeyError:
            raise KeyError(f"environment variable not set: {var.group(1)}")
