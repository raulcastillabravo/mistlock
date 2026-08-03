#!/bin/bash
set -e

PROFILE="localstack"
ROLE_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:role/$LAMBDA_ROLE_NAME"

aws iam create-role --profile $PROFILE \
  --role-name "$LAMBDA_ROLE_NAME" \
  --assume-role-policy-document file://deploy/cli/trust_policy.json

aws dynamodb create-table --profile $PROFILE \
  --table-name "$DYNAMODB_TABLE" \
  --attribute-definitions AttributeName=username,AttributeType=S \
  --key-schema AttributeName=username,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

deploy_function() {
  aws lambda create-function --profile $PROFILE \
    --function-name "$1" \
    --runtime "$LAMBDA_RUNTIME" \
    --role "$ROLE_ARN" \
    --handler "$2" \
    --zip-file "fileb://$3" \
    --environment "Variables={DYNAMODB_TABLE=$DYNAMODB_TABLE}" \
    --timeout 30 \
    --query FunctionArn --output text

  aws lambda wait function-active-v2 --function-name "$1" --profile $PROFILE
}

LOG_USER_ARN=$(deploy_function "$LOG_USER_FUNCTION" log_user.handler dist/log_user.zip)
VALIDATE_EMAIL_ARN=$(deploy_function "$VALIDATE_EMAIL_FUNCTION" validate_email.handler dist/validate_email.zip)

DEFINITION=$(mktemp)
sed -e "s|\${LogUserLambdaArn}|$LOG_USER_ARN|" \
    -e "s|\${ValidateEmailLambdaArn}|$VALIDATE_EMAIL_ARN|" \
    step_function.asl.json > "$DEFINITION"

aws stepfunctions create-state-machine --profile $PROFILE \
  --name "$STEP_FUNCTION_NAME" \
  --definition "file://$DEFINITION" \
  --role-arn "$ROLE_ARN"

rm -f "$DEFINITION"
