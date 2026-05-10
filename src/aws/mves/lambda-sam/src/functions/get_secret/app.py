import os

def lambda_handler(event, context):
    """
    Returns a secret if the provided username matches the admin username.
    """
    admin_username = os.environ.get("ADMIN_USERNAME")
    username = event["queryStringParameters"].get("username")

    if username == admin_username:
        return {
            "statusCode": 200,
            "body": "super-secret-value-from-emulator"
        }
    
    return {
        "statusCode": 403,
        "body": "Forbidden: You do not have access to this secret."
    }
