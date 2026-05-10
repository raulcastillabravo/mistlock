import os
import json
import requests
import boto3
from dotenv import load_dotenv

load_dotenv()

SAM_API_URL: str = os.getenv("SAM_API_URL")
SAM_LAMBDA_URL: str = os.getenv("SAM_LAMBDA_URL")
AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION")

lambda_client = boto3.client(
    "lambda", 
    endpoint_url=SAM_LAMBDA_URL, 
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def test_api():
    print("--- Testing via API Gateway (requests) ---")
    send_request("admin")
    send_request("guest")

def test_lambda():
    print("--- Testing via Lambda SDK (boto3) ---")
    invoke_lambda("admin")
    invoke_lambda("guest")

def send_request(username: str):
    response = requests.get(f"{SAM_API_URL}/get_secret?username={username}")
    print(f"Testing ('{username}'): {response.status_code} - {response.text}")

def invoke_lambda(username: str):
    payload = {"queryStringParameters": {"username": username}}
    
    response = lambda_client.invoke(
        FunctionName="GetSecretFunction",
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response["Payload"].read())
    status_code = response_payload['statusCode']
    body = response_payload['body']

    print(f"Testing ({username}): {status_code} - {body}")

def main():
    test_api()
    print("=" * 40 + "\n")
    test_lambda()

if __name__ == "__main__":
    main()
