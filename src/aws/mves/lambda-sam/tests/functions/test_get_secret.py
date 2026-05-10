import os
import json
import requests
import boto3

API_URL: str = os.getenv("SAM_API_URL")
LAMBDA_URL: str = os.getenv("SAM_LAMBDA_URL")
ENDPOINT: str = f"{API_URL}/get_secret"
AWS_REGION: str = os.getenv("AWS_DEFAULT_REGION")
AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")

def test_get_secret_admin_api(sam_api):
    response = requests.get(ENDPOINT, params={"username": "admin"})
    assert response.status_code == 200
    assert response.text == "super-secret-value-from-emulator"

def test_get_secret_guest_api(sam_api):
    response = requests.get(ENDPOINT, params={"username": "guest"})
    assert response.status_code == 403
    assert "Forbidden" in response.text

def test_get_secret_admin_boto3(sam_lambda):
    response_payload = _invoke_lambda("admin")
    assert response_payload["statusCode"] == 200
    assert response_payload["body"] == "super-secret-value-from-emulator"

def test_get_secret_guest_boto3(sam_lambda):
    response_payload = _invoke_lambda("guest")
    assert response_payload["statusCode"] == 403
    assert "Forbidden" in response_payload["body"]

def _invoke_lambda(username: str):
    client = boto3.client(
        "lambda", 
        endpoint_url=LAMBDA_URL, 
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    payload = {
        "queryStringParameters": {
            "username": username
        }
    }
    response = client.invoke(
        FunctionName="GetSecretFunction",
        Payload=json.dumps(payload)
    )
    return json.loads(response["Payload"].read())