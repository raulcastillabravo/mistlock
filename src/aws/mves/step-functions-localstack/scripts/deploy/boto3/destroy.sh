#!/bin/bash
set -e

PYTHONPATH=. .venv/bin/python deploy/boto3/destroy.py
