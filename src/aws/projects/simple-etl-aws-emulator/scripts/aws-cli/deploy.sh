#!/bin/bash
set -e

.venv/bin/python deploy/utils/package_lambda.py

# 1. DynamoDB table
TABLE_ARN=$(aws dynamodb create-table \
  --table-name "$DYNAMODB_TABLE_NAME" \
  --attribute-definitions AttributeName=file_id,AttributeType=S \
  --key-schema AttributeName=file_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --query TableDescription.TableArn --output text)
aws dynamodb wait table-exists --table-name "$DYNAMODB_TABLE_NAME"

# 2. IAM role that the Lambda assumes, with its permissions
ROLE_ARN=$(aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' \
  --query Role.Arn --output text)
aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name "$ROLE_NAME" \
  --policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {\"Effect\": \"Allow\", \"Action\": [\"s3:GetObject\", \"s3:ListBucket\"], \"Resource\": [\"arn:aws:s3:::$BUCKET_NAME\", \"arn:aws:s3:::$BUCKET_NAME/*\"]},
      {\"Effect\": \"Allow\", \"Action\": [\"dynamodb:PutItem\", \"dynamodb:GetItem\"], \"Resource\": \"$TABLE_ARN\"},
      {\"Effect\": \"Allow\", \"Action\": [\"logs:CreateLogGroup\", \"logs:CreateLogStream\", \"logs:PutLogEvents\"], \"Resource\": \"arn:aws:logs:*:*:*\"}
    ]
  }"

# 3. S3 bucket
aws s3 mb "s3://$BUCKET_NAME"

# 4. Lambda function
FUNCTION_ARN=$(aws lambda create-function \
  --function-name "$FUNCTION_NAME" \
  --runtime python3.14 \
  --role "$ROLE_ARN" \
  --handler handler.lambda_handler \
  --zip-file "fileb://$LAMBDA_ZIP" \
  --timeout 30 \
  --environment "Variables={DYNAMODB_TABLE_NAME=$DYNAMODB_TABLE_NAME}" \
  --query FunctionArn --output text)
aws lambda wait function-active-v2 --function-name "$FUNCTION_NAME"

# 5. S3 trigger: allow S3 to invoke the Lambda, then notify on new objects
aws lambda add-permission \
  --function-name "$FUNCTION_NAME" \
  --statement-id s3-trigger \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn "arn:aws:s3:::$BUCKET_NAME" > /dev/null
aws s3api put-bucket-notification-configuration \
  --bucket "$BUCKET_NAME" \
  --notification-configuration "{\"LambdaFunctionConfigurations\": [{\"LambdaFunctionArn\": \"$FUNCTION_ARN\", \"Events\": [\"s3:ObjectCreated:*\"]}]}"
