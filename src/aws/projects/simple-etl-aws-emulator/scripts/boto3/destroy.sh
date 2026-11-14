#!/bin/bash
set -e

.venv/bin/python -m deploy.boto3.stack destroy
rm -rf deploy/dist
