import os
import pytest
import boto3
from dotenv import load_dotenv

# Garage regenerates the S3 keys on each startup and writes them to .env,
# so load .env first for the connection and override only the buckets.
load_dotenv()
load_dotenv(".env.test", override=True)

@pytest.fixture(scope="session", autouse=True)
def setup_test_s3():
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["S3_ENDPOINT"],
        aws_access_key_id=os.environ["S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET_KEY"],
        region_name=os.environ["AWS_DEFAULT_REGION"],
    )
    buckets = [os.environ["S3_BUCKET_BRONZE"], os.environ["S3_BUCKET_SILVER"]]

    # Create test buckets
    for bucket in buckets:
        try:
            s3.create_bucket(Bucket=bucket)
        except s3.exceptions.BucketAlreadyOwnedByYou:
            pass

    yield

    # Cleanup test buckets
    for bucket in buckets:
        objects = s3.list_objects_v2(Bucket=bucket)

        # Delete all objects in the bucket
        for obj in objects.get("Contents", []):
            s3.delete_object(Bucket=bucket, Key=obj["Key"])

        s3.delete_bucket(Bucket=bucket)
