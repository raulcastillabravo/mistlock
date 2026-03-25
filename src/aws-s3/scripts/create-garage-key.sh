#!/usr/bin/env bash

set -e

GARAGE_CMD="docker exec garage /garage"

# Clean up existing keys with the same name to avoid duplicates
$GARAGE_CMD key list | (grep 'dev-key' || true) | awk '{print $1}' | while read -r id; do
    echo "Deleting existing key $id..."
    $GARAGE_CMD key delete "$id" --yes || true
done

# Create API Key using docker exec
echo "Creating API Key in Garage container..."
KEY_INFO=$($GARAGE_CMD json-api CreateKey '{"name":"dev-key"}')
ACCESS_KEY=$(echo "$KEY_INFO" | jq -r .accessKeyId)
SECRET_KEY=$(echo "$KEY_INFO" | jq -r .secretAccessKey)

# Grant bucket creation permission to the key
$GARAGE_CMD key allow dev-key --create-bucket

# Update .env
ENV_FILE=".env"
echo "Updating $ENV_FILE with credentials..."

upsert_env_var() {
    local key=$1
    local value=$2
    if grep -q "^${key}=" "$ENV_FILE"; then
        sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    else
        echo "${key}=${value}" >> "$ENV_FILE"
    fi
}

upsert_env_var "S3_ACCESS_KEY" "$ACCESS_KEY"
upsert_env_var "S3_SECRET_KEY" "$SECRET_KEY"

echo "Garage key setup completed."
