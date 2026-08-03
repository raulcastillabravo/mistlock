import os

from dotenv import load_dotenv

from src.definition import render_definition
from src.functions import FUNCTIONS
from src.providers.dynamo_db import DynamoDb
from src.providers.iam import Iam
from src.providers.lambda_functions import LambdaFunctions
from src.providers.step_functions import StepFunctions

load_dotenv()


def main():
    print("Creating IAM role and DynamoDB table...")
    Iam().create_role()
    DynamoDb().create_table()

    print("Deploying Lambdas...")
    lambda_functions = LambdaFunctions()
    env_vars = {"DYNAMODB_TABLE": os.getenv("DYNAMODB_TABLE")}
    arns = {
        key: lambda_functions.deploy(
            os.getenv(function["env_var"]),
            function["zip_path"],
            function["handler"],
            env_vars,
        )
        for key, function in FUNCTIONS.items()
    }

    print("Creating the Step Function...")
    StepFunctions().create(render_definition(arns))
    print("Stack deployed")


if __name__ == "__main__":
    main()
