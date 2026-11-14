#!/bin/bash
set -e

.venv/bin/python deploy/utils/package_lambda.py
.venv/bin/python -m deploy.boto3.stack deploy
