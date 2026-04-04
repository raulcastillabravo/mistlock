import os
import boto3
import json
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:4566")
BUCKET_NAME = os.getenv("BUCKET_NAME", "test-bucket")
FUNCTION_NAME = "upload-to-s3"
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# AWS Session Configuration
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=AWS_REGION
)

lambda_client = session.client('lambda', endpoint_url=ENDPOINT_URL)
s3_client = session.client('s3', endpoint_url=ENDPOINT_URL)

def main():
    """Invoke Lambda and verify S3 upload."""
    payload = {
        "bucket_name": BUCKET_NAME,
        "key": "hello.txt",
        "body": "Hello from Lambda!"
    }
    
    print(f"\nInvoking Lambda function '{FUNCTION_NAME}'...")
    response = lambda_client.invoke(
        FunctionName=FUNCTION_NAME,
        Payload=json.dumps(payload)
    )
    
    result = json.loads(response['Payload'].read())
    print(f"✓ Lambda response: {result}")
    
    # Wait for S3 consistency in LocalStack
    time.sleep(1)
    
    print(f"✓ Verifying '{BUCKET_NAME}/hello.txt'...")
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key="hello.txt")
    print(f"✓ Content: {obj['Body'].read().decode('utf-8')}")

if __name__ == "__main__":
    print(f"Connecting to LocalStack at {ENDPOINT_URL}...")
    main()
    print("\nDemonstration completed.")
