import random

from src.providers.dynamo_db import DynamoDb
from src.providers.step_functions import StepFunctions

NUMBER = random.randint(0, 10000)
PAYLOAD = {
    "username": f"testuser_{NUMBER}",
    "email": f"testuser_{NUMBER}@example.com",
}


def test_step_functions(stack):
    step_functions = StepFunctions()
    execution = step_functions.wait(step_functions.start_execution(PAYLOAD))

    assert execution["status"] == "SUCCEEDED"

    usernames = [item["username"]["S"] for item in DynamoDb().scan()]
    assert PAYLOAD["username"] in usernames
