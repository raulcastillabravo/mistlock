#!/bin/bash
set -e

export PATH="$HOME/.local/share/mise/shims:$PATH"

set -a
source .env
set +a

PROFILE="localstack"
STACK_NAME="user-onboarding-stack"
CODE_BUCKET="user-onboarding-code"

aws s3 mb "s3://$CODE_BUCKET" --profile $PROFILE
aws s3 cp dist/log_user.zip "s3://$CODE_BUCKET/log_user.zip" --profile $PROFILE
aws s3 cp dist/validate_email.zip "s3://$CODE_BUCKET/validate_email.zip" \
  --profile $PROFILE

aws cloudformation deploy --profile $PROFILE \
  --stack-name $STACK_NAME \
  --template-file deploy/cloudformation/template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    RoleName="$LAMBDA_ROLE_NAME" \
    TableName="$DYNAMODB_TABLE" \
    LogUserFunctionName="$LOG_USER_FUNCTION" \
    ValidateEmailFunctionName="$VALIDATE_EMAIL_FUNCTION" \
    StateMachineName="$STEP_FUNCTION_NAME" \
    Runtime="$LAMBDA_RUNTIME" \
    CodeBucket="$CODE_BUCKET"
