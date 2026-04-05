import boto3
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class MinioClient:
    _s3_client = None

    def __init__(self):
        self._s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
            aws_access_key_id=os.getenv("MINIO_ROOT_USER", "minioadmin"),
            aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
        )

    def create_bucket(self, bucket_name: str) -> None:
        self._s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")

    def upload_file(self, file_name: str, bucket: str, object_name: Optional[str] = None) -> None:
        if object_name is None:
            object_name = os.path.basename(file_name)
        self._s3_client.upload_file(file_name, bucket, object_name)
        print(f"File '{file_name}' uploaded to '{bucket}/{object_name}'.")

    def download_file(self, bucket: str, object_name: str, file_name: str) -> None:
        self._s3_client.download_file(bucket, object_name, file_name)
        print(f"File '{bucket}/{object_name}' downloaded to '{file_name}'.")

    def delete_file(self, bucket: str, object_name: str) -> None:
        self._s3_client.delete_object(Bucket=bucket, Key=object_name)
        print(f"File '{bucket}/{object_name}' deleted.")
