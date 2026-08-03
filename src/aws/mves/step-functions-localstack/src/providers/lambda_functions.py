import os

import boto3
from dotenv import load_dotenv

from src.providers.boto_config import get_boto_config
from src.providers.iam import get_role_arn

load_dotenv()


class LambdaFunctions:
    _client = None
    _runtime: str = None

    def __init__(self):
        self._client = boto3.client("lambda", **get_boto_config())
        self._runtime = os.getenv("LAMBDA_RUNTIME")

    def deploy(
        self, name: str, zip_path: str, handler: str, env_vars: dict
    ) -> str:
        """zip_path example: 'dist/log_user.zip'."""
        try:
            self.delete(name)
        except self._client.exceptions.ResourceNotFoundException:
            pass

        with open(zip_path, "rb") as artifact:
            function = self._client.create_function(
                FunctionName=name,
                Runtime=self._runtime,
                Role=get_role_arn(),
                Handler=handler,
                Code={"ZipFile": artifact.read()},
                Environment={"Variables": env_vars},
                Timeout=30,
            )

        self._client.get_waiter("function_active_v2").wait(FunctionName=name)
        return function["FunctionArn"]

    def delete(self, name: str) -> None:
        self._client.delete_function(FunctionName=name)
