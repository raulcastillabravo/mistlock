#!/bin/bash
set -e

# Load environment variables
set -a; . .env; set +a

# Start services in the background
sam local start-api > /dev/null 2>&1 &
API_PID=$!

sam local start-lambda > /dev/null 2>&1 &
LAMBDA_PID=$!

# Ensure the background processes are terminated on exit
trap 'kill $API_PID $LAMBDA_PID || true' EXIT

echo "Waiting for SAM services to start..."
for i in {1..30}; do
  curl -s $SAM_API_URL > /dev/null && curl -s $SAM_LAMBDA_URL > /dev/null && break
  sleep 1
done

# Execute main script
.venv/bin/python main.py
