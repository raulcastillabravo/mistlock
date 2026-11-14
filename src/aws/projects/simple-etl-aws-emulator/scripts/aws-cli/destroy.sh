#!/bin/bash
set -e

aws s3 rb "s3://$BUCKET_NAME" --force
aws lambda delete-function --function-name "$FUNCTION_NAME" > /dev/null
aws iam delete-role-policy --role-name "$ROLE_NAME" --policy-name "$ROLE_NAME"
aws iam delete-role --role-name "$ROLE_NAME"
aws dynamodb delete-table --table-name "$DYNAMODB_TABLE_NAME" > /dev/null
aws dynamodb wait table-not-exists --table-name "$DYNAMODB_TABLE_NAME"
rm -rf deploy/dist
