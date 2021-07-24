import os

import boto3

from Uploader import Uploader


class DynamoDB(Uploader):
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=os.environ['AWS_REGION_NAME']
        )
        self.db = self.session.resource('dynamodb')
        self.table = self.db.Table(os.environ['AWS_DYNAMODB_DBNAME'])

    def upload(self, data: dict):
        self.table.put_item(Item=data)
