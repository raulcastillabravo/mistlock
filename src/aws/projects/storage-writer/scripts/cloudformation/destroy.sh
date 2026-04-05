#!/bin/bash
set -e

STACK_NAME="aws-lambda-stack"
DEPLOY_BUCKET="lambda-deploy-bucket"
PROFILE="localstack"

aws cloudformation delete-stack --stack-name $STACK_NAME --profile $PROFILE
aws s3 rb s3://$DEPLOY_BUCKET --force --profile $PROFILE
rm -f deploy/dist/function.zip
