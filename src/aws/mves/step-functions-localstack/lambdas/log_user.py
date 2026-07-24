import os
from datetime import datetime

import boto3

# LocalStack injects AWS_ENDPOINT_URL into the Lambda environment
endpoint_url = os.getenv("AWS_ENDPOINT_URL")

dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def handler(event, context):
    """Log user creation to DynamoDB."""
    table.put_item(
        Item={
            "username": event.get("username"),
            "email": event.get("email"),
            "created_at": datetime.now().isoformat(),
        }
    )

    return {"status": "Logged", "username": event.get("username")}
