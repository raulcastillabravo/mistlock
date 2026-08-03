import os

from dotenv import load_dotenv

load_dotenv()


def get_boto_config() -> dict:
    """boto3 client configuration pointing to LocalStack."""
    return {
        "endpoint_url": os.getenv("LOCALSTACK_ENDPOINT"),
        "region_name": os.getenv("AWS_REGION"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
