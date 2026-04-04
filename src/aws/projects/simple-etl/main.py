import os
import boto3
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:4566")
BUCKET_NAME = os.getenv("BUCKET_NAME", "file-uploads-bucket")
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "file-logs")

AWS_CONF = {
    "endpoint_url": ENDPOINT_URL,
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": "us-east-1"
}

s3 = boto3.client('s3', **AWS_CONF)
dynamodb = boto3.resource('dynamodb', **AWS_CONF)

def upload_sample_files():
    print(f"\nUploading files to {BUCKET_NAME}...")
    sample_files = [
        ("document.pdf", b"Sample PDF content", "application/pdf"),
        ("image.jpg", b"Sample image data", "image/jpeg"),
        ("data.json", b'{"status": "ok"}', "application/json")
    ]
    
    for name, content, ctype in sample_files:
        s3.put_object(Bucket=BUCKET_NAME, Key=name, Body=content, ContentType=ctype)
        print(f"✓ Uploaded: {name}")

def view_logs():
    print(f"\nFile logs from {TABLE_NAME}:")
    items = dynamodb.Table(TABLE_NAME).scan().get('Items', [])
    
    for item in sorted(items, key=lambda x: x.get('upload_timestamp', ''), reverse=True):
        print(f"- {item.get('file_name')} | {item.get('file_size')} bytes | {item.get('upload_timestamp')}")

if __name__ == "__main__":
    upload_sample_files()
    time.sleep(2)
    view_logs()
    print("\nDemonstration completed.")
