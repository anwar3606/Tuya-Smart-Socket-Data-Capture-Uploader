import asyncio
import datetime
import logging
import sys
import time

from Device import TuyaSmartSocket
from DynamoDBUploader import DynamoDB
from InfluxDBUploader import InfluxDB

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout)

device = TuyaSmartSocket()
dynamodb = DynamoDB()
influxdb = InfluxDB()


def generate():
    try:
        data = device.get_data()
        logging.info('Data found: %s', data)
    except Exception:
        logging.error('Missing data!')
        return

    influxdb.upload(data)

    dynamodb.upload({
        'date': str(datetime.datetime.utcnow().date()),
        'time': str(datetime.datetime.utcnow().time()),
        **data
    })


def run_every_one_sec():
    start_time = time.time()
    while True:
        duration = time.time() - start_time
        if duration >= 1:
            start_time = time.time()
            generate()


asyncio.run(run_every_one_sec())
