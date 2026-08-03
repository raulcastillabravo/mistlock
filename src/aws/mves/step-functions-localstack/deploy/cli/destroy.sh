#!/bin/bash
set -e

PROFILE="localstack"
STATE_MACHINE_ARN="arn:aws:states:$AWS_REGION:$AWS_ACCOUNT_ID:stateMachine:$STEP_FUNCTION_NAME"

aws stepfunctions delete-state-machine \
  --state-machine-arn "$STATE_MACHINE_ARN" --profile $PROFILE
aws lambda delete-function --function-name "$LOG_USER_FUNCTION" --profile $PROFILE
aws lambda delete-function --function-name "$VALIDATE_EMAIL_FUNCTION" --profile $PROFILE
aws dynamodb delete-table --table-name "$DYNAMODB_TABLE" --profile $PROFILE
aws iam delete-role --role-name "$LAMBDA_ROLE_NAME" --profile $PROFILE
