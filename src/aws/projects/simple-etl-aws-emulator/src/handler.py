import os
from datetime import datetime, timezone
from urllib.parse import unquote_plus

import boto3


s3 = boto3.client("s3")
table = boto3.resource("dynamodb").Table(os.environ["DYNAMODB_TABLE_NAME"])


def lambda_handler(event: dict, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        head = s3.head_object(Bucket=bucket, Key=key)

        table.put_item(Item={
            "file_id": f"{bucket}/{key}",
            "file_name": key,
            "file_size": record["s3"]["object"]["size"],
            "bucket_name": bucket,
            "content_type": head["ContentType"],
            "upload_timestamp": datetime.now(timezone.utc).isoformat(),
        })
        print(f"Logged: {key}")
