import os

import boto3
from dotenv import load_dotenv

from src.providers.boto_config import get_boto_config

load_dotenv()


class DynamoDb:
    _client = None
    _table_name: str = None

    def __init__(self):
        self._client = boto3.client("dynamodb", **get_boto_config())
        self._table_name = os.getenv("DYNAMODB_TABLE")

    def create_table(self) -> None:
        try:
            self._client.create_table(
                TableName=self._table_name,
                KeySchema=[{"AttributeName": "username", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "username", "AttributeType": "S"}
                ],
                BillingMode="PAY_PER_REQUEST",
            )
        except self._client.exceptions.ResourceInUseException:
            return

        waiter = self._client.get_waiter("table_exists")
        waiter.wait(TableName=self._table_name)

    def delete_table(self) -> None:
        self._client.delete_table(TableName=self._table_name)

    def scan(self) -> list[dict]:
        return self._client.scan(TableName=self._table_name)["Items"]
