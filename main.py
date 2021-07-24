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
    start_time = time.time()
    data = device.get_data()
    duration = time.time() - start_time
    logging.info('Device took: %.2f second', duration)

    logging.info('Data found: %s', data)

    start_time = time.time()
    influxdb.upload(data)
    duration = time.time() - start_time
    logging.info('InfluxDB took: %.2f second', duration)

    start_time = time.time()
    dynamodb.upload({
        'date': str(datetime.datetime.utcnow().date()),
        'time': str(datetime.datetime.utcnow().time()),
        **data
    })
    duration = time.time() - start_time
    logging.info('DynamoDB took: %.2f second', duration)


def run_every_one_sec():
    start_time = time.time()
    while True:
        duration = time.time() - start_time
        if duration >= 1:
            start_time = time.time()
            generate()


asyncio.run(run_every_one_sec())
