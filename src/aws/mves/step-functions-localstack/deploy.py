import boto3
import json
import os
from dotenv import load_dotenv
from utils import create_lambda_zip, get_boto_config, deploy_lambda

load_dotenv()
config = get_boto_config()

def deploy():
    # 1. DynamoDB
    db = boto3.resource("dynamodb", **config)
    try:
        db.create_table(
            TableName=os.getenv("DYNAMODB_TABLE"),
            KeySchema=[{"AttributeName": "username", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "username", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
        print("DynamoDB table created.")
    except db.meta.client.exceptions.ResourceInUseException: pass

    # 2. Lambdas
    lambda_client = boto3.client("lambda", **config)
    role_arn = "arn:aws:iam::000000000000:role/lambda-role"
    arns = {}
    env = {"DYNAMODB_TABLE": os.getenv("DYNAMODB_TABLE", "UserLogs")}

    for name in ["log_user", "validate_email"]:
        func_name = f"{name.replace('_', '-').title().replace('-', '')}Lambda"
        zip_content = create_lambda_zip(f"lambdas/{name}.py")
        
        arns[f"{func_name}Arn"] = deploy_lambda(
            client=lambda_client,
            name=func_name,
            handler=f"{name}.handler",
            zip_data=zip_content,
            role=role_arn,
            env_vars=env
        )

    # 3. Step Function
    sfn = boto3.client("stepfunctions", **config)
    with open("step_function.asl.json") as f:
        asl = f.read()
        for key, arn in arns.items():
            asl = asl.replace(f"${{{key}}}", arn)

    try:
        sfn.create_state_machine(
            name=os.getenv("STEP_FUNCTION_NAME"),
            definition=asl,
            roleArn=role_arn
        )
        print("Step Function created.")
    except sfn.exceptions.StateMachineAlreadyExists:
        sm_arn = f"arn:aws:states:{config['region_name']}:000000000000:stateMachine:{os.getenv('STEP_FUNCTION_NAME')}"
        sfn.update_state_machine(stateMachineArn=sm_arn, definition=asl)
        print("Step Function updated.")

if __name__ == "__main__":
    deploy()
