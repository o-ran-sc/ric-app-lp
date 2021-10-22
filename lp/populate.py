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
This will be used before the LP xApp can read cell measurements from KPM, while now it reads directly from influxDB, or a fake data source
"""

import pandas as pd
from influxdb import DataFrameClient
import datetime


class INSERTDATA:

    def __init__(self):
        host = 'r4-influxdb.ricplt'
        self.client = DataFrameClient(host, '8086', 'root', 'root')
        self.dropdb('CellData')
        self.createdb('CellData')

    def createdb(self, dbname):
        print("Create database: " + dbname)
        self.client.create_database(dbname)
        self.client.switch_database(dbname)

    def dropdb(self, dbname):
        print("DROP database: " + dbname)
        self.client.drop_database(dbname)

    def dropmeas(self, measname):
        print("DROP MEASUREMENT: " + measname)
        self.client.query('DROP MEASUREMENT '+measname)

def time(df):
    df.index = pd.date_range(start=datetime.datetime.now(), freq='10ms', periods=len(df))
    df['measTimeStampRf'] = df['measTimeStampRf'].apply(lambda x: str(x))
    return df

def populatedb():
    data = pd.read_csv('lp/cells.csv')
    data = time(data)

    # inintiate connection and create database UEDATA
    db = INSERTDATA()
    db.client.write_points(data, 'cellMeas')
    del data
