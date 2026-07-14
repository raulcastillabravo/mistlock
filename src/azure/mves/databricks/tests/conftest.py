import os

import boto3
import pytest
from dotenv import load_dotenv

from src.databricks_shim.connect import get_spark_session

load_dotenv()
load_dotenv(".env.test", override=True)


@pytest.fixture(scope="session", autouse=True)
def test_bucket():
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["AWS_ENDPOINT_URL"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"],
    )
    bucket = os.environ["BUCKET_NAME"]

    try:
        s3.create_bucket(Bucket=bucket)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass

    yield

    objects = s3.list_objects_v2(Bucket=bucket)
    for obj in objects.get("Contents", []):
        s3.delete_object(Bucket=bucket, Key=obj["Key"])
    s3.delete_bucket(Bucket=bucket)


@pytest.fixture(scope="session")
def spark():
    session = get_spark_session("Tests")
    yield session
    session.stop()
