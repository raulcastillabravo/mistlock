import os
from boto3 import client

class S3Boto:
    _s3_client: client = None

    def __init__(self):
        endpoint_url: str = os.environ["S3_ENDPOINT"]
        access_key: str = os.environ["S3_ACCESS_KEY"]
        secret_key: str = os.environ["S3_SECRET_KEY"]
        region: str = os.environ["AWS_DEFAULT_REGION"]

        self._s3_client = client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_object(self, path: str) -> bytes:
        bucket, key = path.split("/", 1)
        response = self._s3_client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()

    def put_object(self, path: str, body: bytes):
        bucket, key = path.split("/", 1)
        self._s3_client.put_object(Bucket=bucket, Key=key, Body=body)
