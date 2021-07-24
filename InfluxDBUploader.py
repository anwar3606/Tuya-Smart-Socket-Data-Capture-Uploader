import datetime
import os

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS

from Uploader import Uploader


class InfluxDB(Uploader):
    def __init__(self):
        self.client = InfluxDBClient(url=os.environ['INLFUXDB_URL'], token=os.environ['INLFUXDB_TOKEN'])
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)

    def upload(self, data: dict):
        self.write_api.write(
            os.environ['INLFUXDB_BUCKET'],
            os.environ['INLFUXDB_ORG'], {
                'measurement': os.environ['INLFUXDB_MEASUREMENT_NAME'],
                'time': datetime.datetime.utcnow(),
                'fields': data
            })
