import random

from src.providers.step_functions import StepFunctions


def main():
    number = random.randint(0, 10000)
    payload = {
        "username": f"user_{number}",
        "email": f"user_{number}@example.com",
    }

    step_functions = StepFunctions()
    print(f"Starting workflow for {payload['username']}...")
    execution = step_functions.wait(step_functions.start_execution(payload))

    print(f"Workflow finished with status: {execution['status']}")
    print(f"Details: {execution.get('output') or execution.get('cause')}")


if __name__ == "__main__":
    main()
