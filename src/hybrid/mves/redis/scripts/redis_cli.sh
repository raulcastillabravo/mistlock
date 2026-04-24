#!/bin/bash
set -a
source .env
set +a

docker exec -it redis redis-cli -a "$REDIS_PASSWORD" "$@"
