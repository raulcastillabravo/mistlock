#!/bin/bash
# Registers the Debezium outbox connector in Kafka Connect (or updates it).
set -e

CONFIG=$(python3 -c "import json; print(json.dumps(json.load(open('connect/outbox-connector.json'))['config']))")

curl -s -X PUT -H "Content-Type: application/json" --data "$CONFIG" \
  "http://127.0.0.1:${CONNECT_PORT:-8083}/connectors/trips-outbox/config"
echo
