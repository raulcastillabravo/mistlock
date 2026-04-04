#!/bin/bash
set -e
.venv/bin/python deploy/utils/package_lambda.py
terraform -chdir=deploy/terraform init
terraform -chdir=deploy/terraform apply -auto-approve
