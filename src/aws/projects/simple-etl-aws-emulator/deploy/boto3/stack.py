import os
import sys

import boto3
from dotenv import load_dotenv

from deploy.boto3.policies import permissions_policy, trust_policy


class Stack:
    """S3 bucket whose uploads trigger a Lambda that logs to DynamoDB."""

    _bucket: str = None
    _table: str = None
    _function: str = None
    _role: str = None
    _zip_path: str = None

    def __init__(self):
        self._bucket = os.environ["BUCKET_NAME"]
        self._table = os.environ["DYNAMODB_TABLE_NAME"]
        self._function = os.environ["FUNCTION_NAME"]
        self._role = os.environ["ROLE_NAME"]
        self._zip_path = os.environ["LAMBDA_ZIP"]

    def deploy(self):
        if self._is_deployed():
            print(f"✓ Already deployed: {self._table} exists, nothing to do")
            return
        table_arn = self._create_table()
        role_arn = self._create_role(table_arn)
        boto3.client("s3").create_bucket(Bucket=self._bucket)
        function_arn = self._create_function(role_arn)
        self._add_trigger(function_arn)
        print(f"✓ Deployed: {self._bucket} → {self._function} → {self._table}")

    def destroy(self):
        boto3.resource("s3").Bucket(self._bucket).objects.all().delete()
        boto3.client("s3").delete_bucket(Bucket=self._bucket)
        boto3.client("lambda").delete_function(FunctionName=self._function)
        iam = boto3.client("iam")
        iam.delete_role_policy(RoleName=self._role, PolicyName=self._role)
        iam.delete_role(RoleName=self._role)
        dynamodb = boto3.client("dynamodb")
        dynamodb.delete_table(TableName=self._table)
        dynamodb.get_waiter("table_not_exists").wait(TableName=self._table)
        print(f"✓ Destroyed: {self._bucket}, {self._function}, {self._table}")

    def _is_deployed(self) -> bool:
        dynamodb = boto3.client("dynamodb")
        try:
            dynamodb.describe_table(TableName=self._table)
            return True
        except dynamodb.exceptions.ResourceNotFoundException:
            return False

    def _create_table(self) -> str:
        dynamodb = boto3.client("dynamodb")
        table = dynamodb.create_table(
            TableName=self._table,
            KeySchema=[{"AttributeName": "file_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "file_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        dynamodb.get_waiter("table_exists").wait(TableName=self._table)
        return table["TableDescription"]["TableArn"]

    def _create_role(self, table_arn: str) -> str:
        iam = boto3.client("iam")
        role = iam.create_role(
            RoleName=self._role, AssumeRolePolicyDocument=trust_policy()
        )
        iam.put_role_policy(
            RoleName=self._role,
            PolicyName=self._role,
            PolicyDocument=permissions_policy(self._bucket, table_arn),
        )
        return role["Role"]["Arn"]

    def _create_function(self, role_arn: str) -> str:
        awslambda = boto3.client("lambda")
        with open(self._zip_path, "rb") as zip_file:
            function = awslambda.create_function(
                FunctionName=self._function,
                Runtime="python3.12",
                Role=role_arn,
                Handler="handler.lambda_handler",
                Code={"ZipFile": zip_file.read()},
                Environment={
                    "Variables": {"DYNAMODB_TABLE_NAME": self._table}
                },
                Timeout=30,
            )
        waiter = awslambda.get_waiter("function_active_v2")
        waiter.wait(FunctionName=self._function)
        return function["FunctionArn"]

    def _add_trigger(self, function_arn: str):
        boto3.client("lambda").add_permission(
            FunctionName=self._function,
            StatementId="s3-trigger",
            Action="lambda:InvokeFunction",
            Principal="s3.amazonaws.com",
            SourceArn=f"arn:aws:s3:::{self._bucket}",
        )
        boto3.client("s3").put_bucket_notification_configuration(
            Bucket=self._bucket,
            NotificationConfiguration={"LambdaFunctionConfigurations": [{
                "LambdaFunctionArn": function_arn,
                "Events": ["s3:ObjectCreated:*"],
            }]},
        )


if __name__ == "__main__":
    load_dotenv()
    getattr(Stack(), sys.argv[1])()
