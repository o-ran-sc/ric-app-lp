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
import json
import time
from contextlib import suppress
from lp import main, sdl
from ricxappframe.xapp_frame import Xapp

mock_lp_xapp = None
# tox.ini sets env var to this value
config_file_path = "/tmp/config.json"

def init_config_file():
    with open(config_file_path, "w") as file:
        file.write('{ "version_int" : 1 }')


def write_config_file():
    # generate an inotify/config event
    with open(config_file_path, "w") as file:
        file.write('{ "version_int" : 2 }')


def test_init_xapp():
    # establish config
    init_config_file()

    # wait a bit then update config
    time.sleep(1)
    write_config_file()

