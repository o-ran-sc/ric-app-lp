# ==================================================================================
#       Copyright (c) 2020 China Mobile Technology (USA) Inc. Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
from setuptools import setup, find_packages

setup(
    name="lp",
    version="0.3.0",
    packages=find_packages(exclude=["tests.*", "tests"]),
    author="O-RAN-SC Community",
    description="Load Predictor Xapp for traffic steering use case",
    url="https://gerrit.o-ran-sc.org/r/admin/repos/ric-app/lp",
    install_requires=["ricxappframe>=1.1.1,<2.0.0", "p5py", "PEP517", "Cython", "numpy >= 1.16.2", "pandas>=1.1.3", "torch==1.13.0", "torchvision==0.15.1", "torchaudio==2.0.1", "influxdb", "schedule>=0.0.0"],
    entry_points={"console_scripts": ["start-lp.py=lp.main:start"]},  
    license="Apache 2.0",
    data_files=[("", ["LICENSE.txt"])],
)
