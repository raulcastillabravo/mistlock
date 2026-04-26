#!/bin/bash
set -a
source .env
set +a

docker exec -it mongodb mongosh -u "$MONGO_USER" -p "$MONGO_PASSWORD" --authenticationDatabase admin "$@"
