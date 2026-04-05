import boto3
import os
from datetime import datetime

# Use LOCALSTACK_HOSTNAME if running inside LocalStack
hostname = os.getenv("LOCALSTACK_HOSTNAME", "localhost")
endpoint_url = f"http://{hostname}:4566"

dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

def handler(event, context):
    """Log user creation to DynamoDB."""
    username = event.get("username")
    email = event.get("email")
    
    table.put_item(Item={
        "username": username,
        "email": email,
        "created_at": datetime.now().isoformat()
    })
    
    return {"status": "Logged", "username": username}
