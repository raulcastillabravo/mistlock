import os
import json

def lambda_handler(event, context):
    """
    AWS Lambda handler that returns a secret if the provided username matches the admin username.
    """
    admin_username = os.environ.get("ADMIN_USERNAME")
    
    query_params = event.get("queryStringParameters") or {}
    username = query_params.get("username")

    if username == admin_username:
        return {
            "statusCode": 200,
            "body": "super-secret-value-from-emulator"
        }
    
    return {
        "statusCode": 403,
        "body": "Forbidden: You do not have access to this secret."
    }
