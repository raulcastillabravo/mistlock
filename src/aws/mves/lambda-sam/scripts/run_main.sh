#!/bin/bash
set -e

# Load environment variables
set -a; . .env; set +a

# Start SAM local API in the background
sam local start-api > /dev/null 2>&1 &
SAM_PID=$!

# Ensure the background process is terminated on exit (SIGTERM for orderly shutdown)
trap 'kill $SAM_PID || true' EXIT

echo "Waiting for SAM local API to start..."
for i in {1..30}; do
  curl -s $SAM_API_URL > /dev/null && break
  sleep 1
done

# Execute main script
.venv/bin/python main.py
