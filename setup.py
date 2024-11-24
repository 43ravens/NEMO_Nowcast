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

"""NEMO_Nowcast -- NEMO ocean model nowcast framework
"""
from setuptools import find_packages, setup

import __pkg_metadata__

try:
    long_description = open("README.rst", "rt").read()
except IOError:
    long_description = ""
install_requires = [
    # see envs/environment-dev.yaml for conda environment dev installation,
    # see requirements.txt for package versions used during recent development
    "arrow",
    "attrs",
    "PyYAML",
    "pyzmq",
    "requests",
    "schedule",
    "sentry-sdk",
    "supervisor",
]
tests_require = ["coverage", "pytest"]
extras_require = {"docs": ["sphinx"]}

setup(
    name=__pkg_metadata__.PROJECT,
    version=__pkg_metadata__.VERSION,
    description=__pkg_metadata__.DESCRIPTION,
    long_description=long_description,
    author="Doug Latornell",
    author_email="doug.latornell@43ravens.ca",
    url="https://nemo-nowcast.readthedocs.io/en/latest/NEMO_Nowcast/",
    license="Apache License, Version 2.0",
    platforms=["Linux"],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    packages=find_packages(),
    zip_safe=False,
)
