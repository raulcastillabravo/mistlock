#!/bin/bash
set -e

.venv/bin/python deploy/utils/package_lambda.py

# CloudFormation reads the Lambda code from S3
aws s3 mb "s3://$CODE_BUCKET_NAME"
aws s3 cp "$LAMBDA_ZIP" "s3://$CODE_BUCKET_NAME/function.zip"

aws cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file deploy/cloudformation/template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    "BucketName=$BUCKET_NAME" \
    "TableName=$DYNAMODB_TABLE_NAME" \
    "FunctionName=$FUNCTION_NAME" \
    "RoleName=$ROLE_NAME" \
    "CodeBucketName=$CODE_BUCKET_NAME"
