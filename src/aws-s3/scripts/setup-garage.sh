#!/usr/bin/env bash

set -e

# Create buckets
echo "Creating buckets..."
garage bucket create bronze || true
garage bucket create silver || true

# Create API Key
echo "Creating API Key..."
KEY_INFO=$(garage json-api CreateKey '{"name":"dev-key"}')
ACCESS_KEY=$(echo $KEY_INFO | jq -r .accessKeyId)
SECRET_KEY=$(echo $KEY_INFO | jq -r .secretAccessKey)

# Allow access to buckets
garage bucket allow bronze --read --write --owner --key $ACCESS_KEY
garage bucket allow silver --read --write --owner --key $ACCESS_KEY

# Save to .env.garage
echo "Saving credentials to .env.garage..."
cat <<EOF > .env.garage
S3_ACCESS_KEY=$ACCESS_KEY
S3_SECRET_KEY=$SECRET_KEY
EOF

echo "Garage setup completed."
