import json
import os

import boto3
from dotenv import load_dotenv

from src.providers.boto_config import get_boto_config

load_dotenv()

ASSUME_ROLE_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": ["lambda.amazonaws.com", "states.amazonaws.com"]
            },
            "Action": "sts:AssumeRole",
        }
    ],
}


def get_role_arn() -> str:
    account_id = os.getenv("AWS_ACCOUNT_ID")
    return f"arn:aws:iam::{account_id}:role/{os.getenv('LAMBDA_ROLE_NAME')}"


class Iam:
    _client = None
    _role_name: str = None

    def __init__(self):
        self._client = boto3.client("iam", **get_boto_config())
        self._role_name = os.getenv("LAMBDA_ROLE_NAME")

    def create_role(self) -> str:
        try:
            role = self._client.create_role(
                RoleName=self._role_name,
                AssumeRolePolicyDocument=json.dumps(ASSUME_ROLE_POLICY),
            )
        except self._client.exceptions.EntityAlreadyExistsException:
            role = self._client.get_role(RoleName=self._role_name)

        return role["Role"]["Arn"]

    def delete_role(self) -> None:
        self._client.delete_role(RoleName=self._role_name)
