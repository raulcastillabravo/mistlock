#!/bin/bash
set -a
source .env
set +a

docker compose exec mongodb mongosh -u "$MONGO_USER" -p "$MONGO_PASSWORD" --authenticationDatabase admin "$@"
