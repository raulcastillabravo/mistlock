import json
import os
import time

import boto3
from dotenv import load_dotenv

from src.providers.boto_config import get_boto_config
from src.providers.iam import get_role_arn

load_dotenv()


class StepFunctions:
    _client = None
    _name: str = None
    _role_arn: str = None
    _arn: str = None

    def __init__(self):
        self._client = boto3.client("stepfunctions", **get_boto_config())
        self._name = os.getenv("STEP_FUNCTION_NAME")
        self._role_arn = get_role_arn()
        self._arn = (
            f"arn:aws:states:{os.getenv('AWS_REGION')}"
            f":{os.getenv('AWS_ACCOUNT_ID')}:stateMachine:{self._name}"
        )

    def create(self, definition: str) -> str:
        try:
            self._client.create_state_machine(
                name=self._name,
                definition=definition,
                roleArn=self._role_arn,
            )
        except self._client.exceptions.StateMachineAlreadyExists:
            self._client.update_state_machine(
                stateMachineArn=self._arn, definition=definition
            )
        return self._arn

    def start_execution(self, payload: dict) -> str:
        execution = self._client.start_execution(
            stateMachineArn=self._arn, input=json.dumps(payload)
        )
        return execution["executionArn"]

    def wait(self, execution_arn: str) -> dict:
        """Polls an execution until it leaves the RUNNING status."""
        while True:
            execution = self._client.describe_execution(
                executionArn=execution_arn
            )
            if execution["status"] != "RUNNING":
                return execution
            time.sleep(1)

    def delete(self) -> None:
        self._client.delete_state_machine(stateMachineArn=self._arn)
