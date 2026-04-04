import json
import boto3
import os
from datetime import datetime
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_TABLE', 'file-logs'))

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            size = record['s3']['object']['size']
            
            res = s3.head_object(Bucket=bucket, Key=key)
            timestamp = datetime.utcnow().isoformat()
            
            dynamodb.put_item(Item={
                'file_id': f"{bucket}/{key}",
                'file_name': key,
                'file_size': size,
                'bucket_name': bucket,
                'upload_timestamp': timestamp,
                'content_type': res.get('ContentType', 'unknown')
            })
            print(f"Logged: {key} ({size} bytes)")
        
        return {'statusCode': 200, 'body': json.dumps('Success')}
    except Exception as e:
        print(f"Error: {e}")
        return {'statusCode': 500, 'body': json.dumps(str(e))}
