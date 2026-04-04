import boto3

# Initialize client outside the handler for connection reuse
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda function that uploads an object to S3.
    
    Args:
        event: Contains bucket_name, key, and body
        context: Lambda context object
    
    Returns:
        dict: Response with statusCode and body
    """
    
    bucket_name = event['bucket_name']
    key = event['key']
    body = event['body']
    
    s3.put_object(Bucket=bucket_name, Key=key, Body=body)
    
    return {
        'statusCode': 200,
        'body': f'Successfully uploaded {key} to {bucket_name}'
    }
