import os
import json
import pytest
import requests
import boto3
from dotenv import load_dotenv

load_dotenv()

_api_url: str = os.getenv("SAM_API_URL")
_lambda_url: str = os.getenv("SAM_LAMBDA_URL")
_endpoint: str = f"{_api_url}/get_secret"

def test_get_secret_admin_api(sam_api):
    """
    Test that admin user can access the secret via API Gateway.
    """
    response = requests.get(_endpoint, params={"username": "admin"})
    
    assert response.status_code == 200
    assert response.text == "super-secret-value-from-emulator"

def test_get_secret_guest_api(sam_api):
    """
    Test that guest user is forbidden from accessing the secret via API Gateway.
    """
    response = requests.get(_endpoint, params={"username": "guest"})
    
    assert response.status_code == 403
    assert "Forbidden" in response.text

def test_get_secret_admin_boto3(sam_lambda):
    """
    Test that admin user can access the secret via direct Lambda invoke.
    """
    client = boto3.client(
        "lambda", 
        endpoint_url=_lambda_url, 
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    
    payload = {
        "queryStringParameters": {
            "username": "admin"
        }
    }
    
    response = client.invoke(
        FunctionName="GetSecretFunction",
        Payload=json.dumps(payload)
    )
    
    response_payload = json.loads(response["Payload"].read())
    
    assert response_payload["statusCode"] == 200
    assert response_payload["body"] == "super-secret-value-from-emulator"

def test_get_secret_guest_boto3(sam_lambda):
    """
    Test that guest user is forbidden from accessing the secret via direct Lambda invoke.
    """
    client = boto3.client(
        "lambda", 
        endpoint_url=_lambda_url, 
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    
    payload = {
        "queryStringParameters": {
            "username": "guest"
        }
    }
    
    response = client.invoke(
        FunctionName="GetSecretFunction",
        Payload=json.dumps(payload)
    )
    
    response_payload = json.loads(response["Payload"].read())
    
    assert response_payload["statusCode"] == 403
    assert "Forbidden" in response_payload["body"]
