import os
import boto3

class S3Boto:
    def __init__(self):
        self.endpoint_url: str = os.environ["S3_ENDPOINT"]
        self.access_key: str = os.environ["S3_ACCESS_KEY"]
        self.secret_key: str = os.environ["S3_SECRET_KEY"]
        self.region: str = os.environ["AWS_DEFAULT_REGION"]

        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )

    def get_object(self, path: str) -> bytes:
        bucket, key = path.split("/", 1)
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()

    def put_object(self, path: str, body: bytes):
        bucket, key = path.split("/", 1)
        self.s3_client.put_object(Bucket=bucket, Key=key, Body=body)
