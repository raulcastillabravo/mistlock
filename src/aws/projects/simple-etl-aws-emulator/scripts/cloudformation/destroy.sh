#!/bin/bash
set -e

# CloudFormation cannot delete a bucket that still holds objects
aws s3 rm "s3://$BUCKET_NAME" --recursive
aws cloudformation delete-stack --stack-name "$STACK_NAME"
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"
aws dynamodb wait table-not-exists --table-name "$DYNAMODB_TABLE_NAME"
aws s3 rb "s3://$CODE_BUCKET_NAME" --force
rm -rf deploy/dist
