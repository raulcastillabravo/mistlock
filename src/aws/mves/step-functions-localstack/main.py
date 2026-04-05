import boto3
import json
import os
import time
import random
from dotenv import load_dotenv
from utils import get_boto_config

load_dotenv()
config = get_boto_config()

def run_workflow(username, email):
    sfn = boto3.client("stepfunctions", **config)
    name = os.getenv('STEP_FUNCTION_NAME')
    region = config['region_name']
    workflow_arn = f"arn:aws:states:{region}:000000000000:stateMachine:{name}"
    
    print(f"🚀 Starting workflow for user: {username} ({email})")
    response = sfn.start_execution(
        stateMachineArn=workflow_arn,
        input=json.dumps({"username": username, "email": email})
    )
    
    execution_arn = response["executionArn"]
    while True:
        status = sfn.describe_execution(executionArn=execution_arn)
        if status["status"] != "RUNNING":
            print(f"🏁 Workflow completed with status: {status['status']}")
            if status["status"] == "SUCCEEDED":
                print("Output:", status.get("output"))
            else:
                print("Error Details:", status.get("cause") or status.get("stopDate"))
            break
        time.sleep(1)

if __name__ == "__main__":
    num = random.randint(0, 10000)
    username = f"user_{num}"
    email = f"user_{num}@example.com"
    run_workflow(username, email)
