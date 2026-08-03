#!/bin/bash
set -e

export PATH="$HOME/.local/share/mise/shims:$PATH"

set -a
source .env
set +a

terraform -chdir=deploy/terraform init -input=false
terraform -chdir=deploy/terraform apply -auto-approve \
  -var "aws_region=$AWS_REGION" \
  -var "endpoint_url=$LOCALSTACK_ENDPOINT" \
  -var "role_name=$LAMBDA_ROLE_NAME" \
  -var "table_name=$DYNAMODB_TABLE" \
  -var "log_user_function=$LOG_USER_FUNCTION" \
  -var "validate_email_function=$VALIDATE_EMAIL_FUNCTION" \
  -var "state_machine_name=$STEP_FUNCTION_NAME" \
  -var "lambda_runtime=$LAMBDA_RUNTIME"
