#!/bin/bash
set -e

set -a; . .env; set +a

# Start Azure Functions in the background
func start --port $FUNCTION_PORT > /dev/null 2>&1 &
trap 'kill -9 $(lsof -t -i:$FUNCTION_PORT) || true' EXIT

echo "Waiting for Azure Functions host to start..."
for i in {1..30}; do
  curl -s http://localhost:$FUNCTION_PORT > /dev/null && break
  sleep 1
done

# There is a delay until the function can respond
sleep 1  

.venv/bin/python main.py
