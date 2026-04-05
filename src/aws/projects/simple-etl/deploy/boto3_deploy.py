import boto3
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration from Environment Variables
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:4566")
BUCKET_NAME = os.getenv("BUCKET_NAME", "file-uploads-bucket")
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "file-logs")
LAMBDA_NAME = "s3-file-processor"
ROLE_NAME = "lambda-s3-processor-role"
ZIP_FILE = "tmp/lambda.zip"

def get_boto3_client(service):
    """Create a boto3 client for a specific service."""
    return boto3.client(service, endpoint_url=ENDPOINT_URL, region_name=REGION)

def deploy():
    """Deploy all resources using boto3."""
    s3 = get_boto3_client("s3")
    dynamodb = get_boto3_client("dynamodb")
    iam = get_boto3_client("iam")
    awslambda = get_boto3_client("lambda")

    # 1. Create DynamoDB Table
    print(f"Creating DynamoDB table '{TABLE_NAME}'...")
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "file_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "file_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    # 2. Create IAM Role for Lambda
    print(f"Creating IAM role '{ROLE_NAME}'...")
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    role = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy)
    )
    role_arn = role["Role"]["Arn"]

    # 3. Create S3 Bucket
    print(f"Creating S3 bucket '{BUCKET_NAME}'...")
    s3.create_bucket(Bucket=BUCKET_NAME)

    # 4. Create Lambda Function
    print(f"Creating Lambda function '{LAMBDA_NAME}'...")
    with open(ZIP_FILE, "rb") as f:
        zipped_code = f.read()

    lambda_response = awslambda.create_function(
        FunctionName=LAMBDA_NAME,
        Runtime="python3.12",
        Role=role_arn,
        Handler="lambda.lambda_handler",
        Code={"ZipFile": zipped_code},
        Environment={"Variables": {"DYNAMODB_TABLE": TABLE_NAME}},
        Timeout=30
    )
    lambda_arn = lambda_response["FunctionArn"]
    print(f"Lambda Created: {lambda_arn}")

    # 5. Add S3 Permission to Lambda
    print("Adding S3 permission to Lambda...")
    awslambda.add_permission(
        FunctionName=LAMBDA_NAME,
        StatementId="s3-trigger",
        Action="lambda:InvokeFunction",
        Principal="s3.amazonaws.com",
        SourceArn=f"arn:aws:s3:::{BUCKET_NAME}"
    )

    # Give LocalStack a moment to propagate permissions
    print("Waiting for permission propagation...")
    time.sleep(2)

    # 6. Configure S3 Notification
    print("Configuring S3 bucket notifications...")
    s3.put_bucket_notification_configuration(
        Bucket=BUCKET_NAME,
        NotificationConfiguration={
            "LambdaFunctionConfigurations": [
                {
                    "LambdaFunctionArn": lambda_arn,
                    "Events": ["s3:ObjectCreated:*"]
                }
            ]
        }
    )

    print("\nDeployment completed successfully!")

if __name__ == "__main__":
    deploy()
