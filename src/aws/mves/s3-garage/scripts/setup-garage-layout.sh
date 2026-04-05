#!/usr/bin/env bash
# Ref: https://git.deuxfleurs.fr/Deuxfleurs/garage/src/branch/main-v2/script/dev-configure.sh

set -e

GARAGE_CMD="docker exec garage /garage"

# Assign layout roles to nodes that have none
echo "Assigning layout roles..."
$GARAGE_CMD status | grep 'NO ROLE' | grep -Po '^[0-9a-f]+' | while read -r id; do
    echo "Assigning role to node $id..."
    $GARAGE_CMD layout assign "$id" -z dc1 -c 1G
done

# Apply layout
echo "Applying layout change..."
$GARAGE_CMD layout apply --version 1 || true

# Wait for healthy cluster
echo "Waiting for healthy cluster..."
until $GARAGE_CMD status 2>&1 | grep -q HEALTHY; do
    sleep 1
done

echo "Garage layout setup completed."
