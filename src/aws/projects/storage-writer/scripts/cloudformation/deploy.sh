#!/bin/bash
set -e

.venv/bin/python deploy/utils/package_lambda.py

STACK_NAME="aws-lambda-stack"
DEPLOY_BUCKET="lambda-deploy-bucket"
PROFILE="localstack"

# 1. Create temporary bucket
aws s3 mb s3://$DEPLOY_BUCKET --profile $PROFILE

# 2. Upload zip
aws s3 cp deploy/dist/function.zip s3://$DEPLOY_BUCKET/lambda.zip --profile $PROFILE

# 3. Deploy stack
aws cloudformation deploy --profile $PROFILE \
  --stack-name $STACK_NAME \
  --template-file deploy/cloudformation/template.yaml \
  --capabilities CAPABILITY_NAMED_IAM
