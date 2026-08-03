#!/bin/bash
set -e

export PATH="$HOME/.local/share/mise/shims:$PATH"

PROFILE="localstack"
STACK_NAME="user-onboarding-stack"
CODE_BUCKET="user-onboarding-code"

aws cloudformation delete-stack --stack-name $STACK_NAME --profile $PROFILE
aws cloudformation wait stack-delete-complete \
  --stack-name $STACK_NAME --profile $PROFILE
aws s3 rb "s3://$CODE_BUCKET" --force --profile $PROFILE
