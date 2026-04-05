#!/bin/bash
set -e
.venv/bin/python deploy/utils/package_lambda.py
.venv/bin/python deploy/boto3/deploy.py
