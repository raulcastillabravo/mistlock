import os

from dotenv import load_dotenv

from src.functions import FUNCTIONS
from src.providers.dynamo_db import DynamoDb
from src.providers.iam import Iam
from src.providers.lambda_functions import LambdaFunctions
from src.providers.step_functions import StepFunctions

load_dotenv()


def main():
    StepFunctions().delete()

    lambda_functions = LambdaFunctions()
    for function in FUNCTIONS.values():
        lambda_functions.delete(os.getenv(function["env_var"]))

    DynamoDb().delete_table()
    Iam().delete_role()
    print("Stack destroyed")


if __name__ == "__main__":
    main()
