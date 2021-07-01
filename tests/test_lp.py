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
from lp.exceptions import UENotFound, CellNotFound
from ricxappframe.xapp_frame import Xapp, RMRXapp
import pytest
import pdb

@pytest.fixture
def ue_metrics():
    return {
        "UEID": "9876543",
        "ServingCellID": "460-7-797-57315",
        "MeasTimestampUEPDCPBytes": "2021-06-20 13:58:29.220",
        "MeasPeriodUEPDCPBytes": 20,
        "UEPDCPBytesDL": 250000,
        "UEPDCPBytesUL": 100000,
        "MeasTimestampUEPRBUsage": "2021-06-20 13:58:29.220",
        "MeasPeriodUEPRBUsage": 20,
        "UEPRBUsageDL": 10,
        "UEPRBUsageUL": 30,
        "MeasTimestampRF": "2021-06-20 13:58:29.210",
        "MeasPeriodRF": 40,
        "ServingCellRF": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
        "NeighborCellRF": [
            {"CID": "460-7-797-57314", "CellRF": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5}},
            {"CID": "460-7-797-57316", "CellRF": {"RSRP": -140, "RSRQ": -17, "RSSINR": -6}},
        ],
        "FAKE_BAD_DATA_TEST": "THIS SHOULD GET DELETED",
    }


@pytest.fixture
def ue_metrics_with_bad_cell():
    return {
        "UEID": "3456789",
        "ServingCellID": "460-7-797-57315",
        "MeasTimestampUEPDCPBytes": "2021-06-20 13:58:29.220",
        "MeasPeriodUEPDCPBytes": 20,
        "UEPDCPBytesDL": 250000,
        "UEPDCPBytesUL": 100000,
        "MeasTimestampUEPRBUsage": "2021-06-20 13:58:29.220",
        "MeasPeriodUEPRBUsage": 20,
        "UEPRBUsageDL": 10,
        "UEPRBUsageUL": 30,
        "MeasTimestampRF": "2021-06-20 13:58:29.210",
        "MeasPeriodRF": 40,
        "ServingCellRF": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
        "NeighborCellRF": [
            {"CID": "460-7-797-57314", "CellRF": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5}},
            {"CID": "CANTTOUCHTHIS", "CellRF": {"RSRP": -140, "RSRQ": -17, "RSSINR": -6}},
        ],
    }


@pytest.fixture
def cell_metrics_1():
    return {
        "CellID": "460-7-797-57314",
        "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
        "MeasPeriodPDCPBytes": 20,
        "PDCPBytesDL": 2000000,
        "PDCPBytesUL": 1200000,
        "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
        "MeasPeriodAvailPRB": 20,
        "AvailPRBDL": 30,
        "AvailPRBUL": 50,
    }


@pytest.fixture
def cell_metrics_2():
    return {
        "CellID": "460-7-797-57315",
        "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
        "MeasPeriodPDCPBytes": 20,
        "PDCPBytesDL": 800000,
        "PDCPBytesUL": 400000,
        "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
        "MeasPeriodAvailPRB": 20,
        "AvailPRBDL": 30,
        "AvailPRBUL": 45,
        "FAKE_BAD_DATA_TEST": "THIS SHOULD GET DELETED",
    }


@pytest.fixture
def cell_metrics_3():
    return {
        "CellID": "460-7-797-57316",
        "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
        "MeasPeriodPDCPBytes": 20,
        "PDCPBytesDL": 1900000,
        "PDCPBytesUL": 1000000,
        "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
        "MeasPeriodAvailPRB": 20,
        "AvailPRBDL": 60,
        "AvailPRBUL": 80,
    }


@pytest.fixture
def good_cell():
    return {
        "PredictionUE": "9876543",
        "UEMeasurements": {
            "ServingCellID": "460-7-797-57315",
            "MeasTimestampUEPDCPBytes": "2021-06-20 13:58:29.220",
            "MeasPeriodUEPDCPBytes": 20,
            "UEPDCPBytesDL": 250000,
            "UEPDCPBytesUL": 100000,
            "MeasTimestampUEPRBUsage": "2021-06-20 13:58:29.220",
            "MeasPeriodUEPRBUsage": 20,
            "UEPRBUsageDL": 10,
            "UEPRBUsageUL": 30,
        },
        "CellMeasurements": [
            {
                "CellID": "460-7-797-57314",
                "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 2000000,
                "PDCPBytesUL": 1200000,
                "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 50,
                "MeasTimestampRF": "2021-06-20 13:58:29.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5},
            },
            {
                "CellID": "460-7-797-57316",
                "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 1900000,
                "PDCPBytesUL": 1000000,
                "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 60,
                "AvailPRBUL": 80,
                "MeasTimestampRF": "2021-06-20 13:58:29.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -140, "RSRQ": -17, "RSSINR": -6},
            },
            {
                "CellID": "460-7-797-57315",
                "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 800000,
                "PDCPBytesUL": 400000,
                "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 45,
                "MeasTimestampRF": "2021-06-20 13:58:29.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
            },
        ],
    }


@pytest.fixture
def bad_cell():
    return {
        "PredictionUE": "3456789",
        "UEMeasurements": {
            "ServingCellID": "460-7-797-57315",
            "MeasTimestampUEPDCPBytes": "2021-06-20 13:58:29.220",
            "MeasPeriodUEPDCPBytes": 20,
            "UEPDCPBytesDL": 250000,
            "UEPDCPBytesUL": 100000,
            "MeasTimestampUEPRBUsage": "2021-06-20 13:58:29.220",
            "MeasPeriodUEPRBUsage": 20,
            "UEPRBUsageDL": 10,
            "UEPRBUsageUL": 30,
        },
        "CellMeasurements": [
            {
                "CellID": "460-7-797-57314",
                "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 2000000,
                "PDCPBytesUL": 1200000,
                "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 50,
                "MeasTimestampRF": "2021-06-20 13:58:29.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5},
            },
            {
                "CellID": "460-7-797-57315",
                "MeasTimestampPDCPBytes": "2021-06-20 13:58:29.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 800000,
                "PDCPBytesUL": 400000,
                "MeasTimestampAvailPRB": "2021-06-20 13:58:29.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 45,
                "MeasTimestampRF": "2021-06-20 13:58:29.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
            },
        ],
    }

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


def test_init_xapp(monkeypatch, ue_metrics, cell_metrics_1, cell_metrics_2, cell_metrics_3, ue_metrics_with_bad_cell, good_cell):

    _original_post_init = main.post_init

    def fake_post_init(self):
        _original_post_init(self)
        self.sdl_set(sdl.UE_NS, "9876543", json.dumps(ue_metrics).encode(), usemsgpack=False)
        self.sdl_set(sdl.UE_NS, "3456789", json.dumps(ue_metrics_with_bad_cell).encode(), usemsgpack=False)
        self.sdl_set(sdl.CELL_NS, "460-7-797-57314", json.dumps(cell_metrics_1).encode(), usemsgpack=False)
        self.sdl_set(sdl.CELL_NS, "460-7-797-57315", json.dumps(cell_metrics_2).encode(), usemsgpack=False)
        self.sdl_set(sdl.CELL_NS, "460-7-797-57316", json.dumps(cell_metrics_3).encode(), usemsgpack=False)
        
        expected=sdl.get_uedata(self, "9876543")
        assert expected==good_cell
        expected=sdl.get_uedata(self, "3456789")
        try:
            sdl.get_uedata(self, "1234567")
        except UENotFound:
            self.logger.warning("UE doesn't exist!")
            

    # patch
    monkeypatch.setattr("lp.main.post_init", fake_post_init)

    # establish config
    init_config_file()

    # start lp
    main.start(thread=True)

    # wait a bit then update config
    time.sleep(1)
    write_config_file()

def test_mock_ts():
    # define a mock traffic steering xapp
    def mock_ts_entry(self):

        # make sure a bad steering request doesn't blow up in lp
        val = "".encode()	# send empty string encoded message
        self.rmr_send(val, 30000)
        val = "just a string".encode()	# not json
        self.rmr_send(val, 30000)
        val = json.dumps({"key": "value"}).encode()  # json but missing UEPredictionSet
        self.rmr_send(val, 30000)

        # valid request body but missing cell id
        val = json.dumps({"UEPredictionSet": ["NOTVALIDUEs"]}).encode()
        self.rmr_send(val, 30000)

        # good traffic steering request
        val = json.dumps({"UEPredictionSet": ["9876543", "3456789"]}).encode()
        self.rmr_send(val, 30000)

        # should trigger the default handler and do nothing
        val = json.dumps({"send other message types": 1}).encode()
        self.rmr_send(val, 60001)

    global mock_ts_xapp
    mock_ts_xapp = Xapp(entrypoint=mock_ts_entry, rmr_port=4564, use_fake_sdl=True)
    mock_ts_xapp.run()  # this will return since entry isn't a loop

def test_rmr_flow(monkeypatch, good_cell, bad_cell):
    """
    this flow mocks out the xapps on both sides of LP.
    It first stands up a mock lp, then it starts up a mock ts
    which will immediately send requests to the running lp driver.
    """

    expected_result = {}

    # define a mock lp predictor
    def mock_lp_default_handler(self, summary, sbuf):
        pass

    def mock_lp_predict_handler(self, summary, sbuf):
        nonlocal expected_result  # closures ftw
        pay = json.loads(summary["payload"])
        expected_result[pay["PredictionUE"]] = pay

    global mock_lp_xapp
    mock_lp_xapp = RMRXapp(mock_lp_default_handler, rmr_port=4666, use_fake_sdl=True)
    mock_lp_xapp.register_callback(mock_lp_predict_handler, 30000)
    mock_lp_xapp.run(thread=True)

    time.sleep(1)

    # define a mock traffic steering xapp
    def mock_ts_entry(self):
        # make sure a bad steering request doesn't blow up in lp
        val = "".encode()       # send empty string encoded message
        self.rmr_send(val, 30000)
        val = "just a string".encode()  # not json
        self.rmr_send(val, 30000)
        val = json.dumps({"key": "value"}).encode()  # json but missing UEPredictionSet
        self.rmr_send(val, 30000)

        # valid request body but missing cell id
        val = json.dumps({"UEPredictionSet": ["NOTVALIDUEs"]}).encode()
        self.rmr_send(val, 30000)

        # good traffic steering request
        val = json.dumps({"UEPredictionSet": ["9876543", "3456789"]}).encode()
        self.rmr_send(val, 30000)

        # should trigger the default handler and do nothing
        val = json.dumps({"send other message types": 1}).encode()
        self.rmr_send(val, 60001)

    global mock_ts_xapp
    mock_ts_xapp = Xapp(entrypoint=mock_ts_entry, rmr_port=4564, use_fake_sdl=True)
    mock_ts_xapp.run()  # this will return since entry isn't a loop

    time.sleep(1)

    assert main.get_stats() == {"DefCalled": 2, "SteeringRequests": 10}

    # break SDL and send traffic again
    def sdl_healthcheck_fails(self):
        return False
    monkeypatch.setattr("ricxappframe.xapp_sdl.SDLWrapper.healthcheck", sdl_healthcheck_fails)
    mock_ts_xapp.run()

    # restore SDL and send traffic once more
    def sdl_healthcheck_passes(self):
        return True
    monkeypatch.setattr("ricxappframe.xapp_sdl.SDLWrapper.healthcheck", sdl_healthcheck_passes)
    mock_ts_xapp.run()


def teardown_module():
    """
    this is like a "finally"; the name of this function is pytest magic
    safer to put down here since certain failures above can lead to pytest never returning
    for example if an exception gets raised before stop is called in any test function above,
    pytest will hang forever
    """
    with suppress(Exception):
        mock_ts_xapp.stop()
    with suppress(Exception):
        mock_lp_xapp.stop()
    with suppress(Exception):
        main.stop()
