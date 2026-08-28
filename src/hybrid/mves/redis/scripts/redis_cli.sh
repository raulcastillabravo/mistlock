#!/bin/bash
set -a
source .env
set +a

docker compose exec redis redis-cli -a "$REDIS_PASSWORD" "$@"
