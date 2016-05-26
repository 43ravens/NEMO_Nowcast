# Copyright 2016 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast framework library functions.
"""
import yaml


def load_config(config_file):
    """Load the YAML config_file and return its contents as a dict.

    The value of config_file is added to the config dict with the key
    :kbd:`config_file`.

    :arg str config_file: Path/name of YAML configuration file for
                          the NEMO nowcast system.

    :returns: config dict
    """
    with open(config_file, 'rt') as f:
        config = yaml.safe_load(f)
    config['config_file'] = config_file
    return config
