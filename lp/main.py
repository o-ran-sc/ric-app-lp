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
"""
lp entrypoint module

RMR Messages
 #define TS_UE_LIST 30000
for now re-use the 30000 to receive a UEID for prediction
"""

import json
from os import getenv
from ricxappframe.xapp_frame import RMRXapp, rmr
from lp import sdl
from lp.exceptions import UENotFound, CellNotFound


# pylint: disable=invalid-name
rmr_xapp = None


def post_init(self):
    """
    Function that runs when xapp initialization is complete
    """
    self.def_hand_called = 0
    self.traffic_steering_requests = 0


def handle_config_change(self, config):
    """
    Function that runs at start and on every configuration file change.
    """
    self.logger.debug("handle_config_change: config: {}".format(config))


def default_handler(self, summary, sbuf):
    """
    Function that processes messages for which no handler is defined
    """
    self.def_hand_called += 1
    self.logger.warning("default_handler unexpected message type {}".format(summary[rmr.RMR_MS_MSG_TYPE]))
    self.rmr_free(sbuf)


def lp_req_handler(self, summary, sbuf):
    """
    This is the main handler for this xapp, which handles load prediction requests.
    This app fetches a set of data from SDL, and calls the predict method to perform
    prediction based on the data

    The incoming message that this function handles looks like:
        {"UEPredictionSet" : ["UEId1","UEId2","UEId3"]}
    """
    self.traffic_steering_requests += 1
    # we don't use rts here; free the buffer
    self.rmr_free(sbuf)

    ue_list = []
    try:
        req = json.loads(summary[rmr.RMR_MS_PAYLOAD])  # input should be a json encoded as bytes
        ue_list = req["UEPredictionSet"]
        self.logger.debug("lp_req_handler processing request for UE list {}".format(ue_list))
    except (json.decoder.JSONDecodeError, KeyError):
        self.logger.warning("lp_req_handler failed to parse request: {}".format(summary[rmr.RMR_MS_PAYLOAD]))
        return

    # iterate over the UEs, fetches data for each UE and perform prediction
    for ueid in ue_list:
        try:
            uedata = sdl.get_uedata(self, ueid)
            predict(self, uedata)
        except UENotFound:
            self.logger.warning("lp_req_handler received a TS Request for a UE that does not exist!")

def predict(self, uedata):
    """
    This is the method that's to perform prediction based on a model
    For now it just returns dummy data
    :return:
    """
    return "Overloaded!"

def start(thread=False):
    """
    This is a convenience function that allows this xapp to run in Docker
    for "real" (no thread, real SDL), but also easily modified for unit testing
    (e.g., use_fake_sdl). The defaults for this function are for the Dockerized xapp.
    """
    global rmr_xapp
    fake_sdl = getenv("USE_FAKE_SDL", None)
    rmr_xapp = RMRXapp(default_handler,
                       config_handler=handle_config_change,
                       rmr_port=4560,
                       post_init=post_init,
                       use_fake_sdl=bool(fake_sdl))
    rmr_xapp.register_callback(lp_req_handler, 30000)
    rmr_xapp.run(thread)


def stop():
    """
    can only be called if thread=True when started
    """
    rmr_xapp.stop()


def get_stats():
    """
    hacky for now, will evolve
    """
    return {"DefCalled": rmr_xapp.def_hand_called,
            "SteeringRequests": rmr_xapp.traffic_steering_requests}
