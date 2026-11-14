import os
import time

import boto3


class FilePipeline:
    _bucket: str = None
    _s3 = None
    _table = None

    def __init__(self):
        self._bucket = os.environ["BUCKET_NAME"]
        self._s3 = boto3.client("s3")
        self._table = boto3.resource("dynamodb").Table(
            os.environ["DYNAMODB_TABLE_NAME"]
        )

    def upload(self, key: str, body: bytes, content_type: str):
        self._s3.put_object(
            Bucket=self._bucket, Key=key, Body=body, ContentType=content_type
        )

    def wait_for_log(self, key: str, since: str, timeout: int = 30) -> dict:
        """Poll DynamoDB until the Lambda logs `key` after `since` (ISO 8601)."""
        file_id = f"{self._bucket}/{key}"
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            item = self._get_item(file_id)
            if item and item["upload_timestamp"] >= since:
                return item
            time.sleep(0.5)

        raise TimeoutError(f"No log for {file_id} after {timeout}s")

    def _get_item(self, file_id: str) -> dict | None:
        try:
            return self._table.get_item(Key={"file_id": file_id}).get("Item")
        except self._table.meta.client.exceptions.ResourceNotFoundException:
            # AWS Emulator 1.0.322: GetItem on an empty table created with
            # CloudFormation fails instead of returning no item.
            return None
