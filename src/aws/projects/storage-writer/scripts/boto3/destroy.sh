#!/bin/bash
set -e

PROFILE="localstack"

aws lambda delete-function --function-name upload-to-s3 --profile $PROFILE
aws iam delete-role --role-name lambda-s3-role --profile $PROFILE
aws s3 rb s3://test-bucket --force --profile $PROFILE
rm -f deploy/dist/function.zip
