import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

# Configuration
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:4566")
BUCKET_NAME = os.getenv("BUCKET_NAME", "test-bucket")
LAMBDA_NAME = "upload-to-s3"
ROLE_NAME = "lambda-s3-role"
ZIP_FILE = "deploy/dist/function.zip"

def get_boto3_client(service):
    """Create a boto3 client for a specific service."""
    return boto3.client(service, endpoint_url=ENDPOINT_URL, region_name=REGION)

def deploy():
    """Deploy all resources using boto3."""
    print(f"Connecting to LocalStack...")
    s3 = get_boto3_client("s3")
    iam = get_boto3_client("iam")
    awslambda = get_boto3_client("lambda")

    # 1. Create S3 Bucket
    print(f"Creating S3 bucket '{BUCKET_NAME}'...")
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print(f"✓ Bucket created: {BUCKET_NAME}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"💡 Bucket '{BUCKET_NAME}' already exists.")

    # 2. Create IAM Role for Lambda
    print(f"Creating IAM role '{ROLE_NAME}'...")
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow", 
            "Principal": {"Service": "lambda.amazonaws.com"}, 
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        response = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )
        role_arn = response["Role"]["Arn"]
        print(f"✓ Role created: {ROLE_NAME}")
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=ROLE_NAME)["Role"]["Arn"]
        print(f"💡 Role '{ROLE_NAME}' already exists, skipping creation.")

    # 3. Create Lambda Function
    print(f"Creating Lambda function '{LAMBDA_NAME}'...")
    with open(ZIP_FILE, "rb") as f:
        zipped_code = f.read()

    try:
        awslambda.create_function(
            FunctionName=LAMBDA_NAME,
            Runtime="python3.12",
            Role=role_arn,
            Handler="lambda.lambda_handler",
            Code={"ZipFile": zipped_code},
            Timeout=30
        )
    except awslambda.exceptions.ResourceConflictException:
        print("Function already exists. Updating code...")
        awslambda.update_function_code(
            FunctionName=LAMBDA_NAME,
            ZipFile=zipped_code
        )

    print("\nDeployment completed successfully!")

if __name__ == "__main__":
    deploy()
