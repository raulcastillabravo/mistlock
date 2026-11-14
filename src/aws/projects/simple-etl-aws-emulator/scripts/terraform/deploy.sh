#!/bin/bash
set -e

# Run with `mise run`, which loads .env. Terraform changes directory with
# -chdir, so the emulator file paths must be absolute.
export AWS_SHARED_CREDENTIALS_FILE="$PWD/$AWS_SHARED_CREDENTIALS_FILE"
export AWS_CONFIG_FILE="$PWD/$AWS_CONFIG_FILE"
export AWS_CA_BUNDLE="$PWD/$AWS_CA_BUNDLE"

.venv/bin/python deploy/utils/package_lambda.py
terraform -chdir=deploy/terraform init
terraform -chdir=deploy/terraform apply -auto-approve \
  -var "bucket_name=$BUCKET_NAME" \
  -var "table_name=$DYNAMODB_TABLE_NAME" \
  -var "function_name=$FUNCTION_NAME" \
  -var "role_name=$ROLE_NAME" \
  -var "lambda_zip=$PWD/$LAMBDA_ZIP"
