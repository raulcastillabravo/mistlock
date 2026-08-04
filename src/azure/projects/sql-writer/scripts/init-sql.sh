#!/bin/bash
set -e

# Wait for SQL Edge to be ready
echo "Waiting for SQL Edge to be ready..."
until docker compose exec -T azure-sql-edge /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Password123! -Q "SELECT 1" &> /dev/null
do
  echo -n "."
  sleep 1
done

echo -e "\nInitializing SQL tables..."
docker compose exec -T azure-sql-edge /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Password123! -d master < sql/init.sql

echo "✓ SQL tables initialized successfully!"
