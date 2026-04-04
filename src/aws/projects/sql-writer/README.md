# LocalStack Hybrid Cloud Example

Minimal viable example to demonstrate a hybrid cloud scenario using LocalStack and an external PostgreSQL instance. This example shows how an AWS Lambda (simulated in LocalStack) can retrieve secrets from Secrets Manager and interact with a database outside the AWS environment.

## Project Structure

```
localstack-hybrid-cloud/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── add_user_lambda/          # Lambda function code
│   ├── lambda_handler.py
│   └── models.py
├── docker-compose.yml        # LocalStack + Postgres
├── package_lambda.py         # ZIP builder script
├── main.tf                   # Infrastructure (Secrets + Lambda)
├── terraform.tfvars          # Terraform variables
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- Terraform installed
- AWS CLI installed
- DBeaver or any SQL client (to verify results)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P`
3. Select: **Dev Containers: Reopen in Container**

### Step 2: Configure AWS CLI

If you haven't configured the CLI yet, run:

```bash
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set region us-east-1
```

### Step 3: Prepare and Deploy

```bash
docker compose up -d
python package_lambda.py
terraform init && terraform apply -auto-approve
```

### Step 4: Invoke the Lambda via CLI

```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
    --function-name AddUserFunction \
    --payload '{}' \
    response.json
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Start Infrastructure

```bash
docker compose up -d
```

### Step 2: Build and Deploy

```bash
python package_lambda.py
terraform init && terraform apply -auto-approve
```

### Step 3: Run Application (Invoke Lambda)

```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
    --function-name AddUserFunction \
    --payload '{}' \
    response.json

cat response.json
```

## Verifying Results

Since the Lambda interacts with a local PostgreSQL database, you can verify the results using **DBeaver** or any other database client:

1. **Host**: `localhost`
2. **Port**: `5432`
3. **Database**: `mydb`
4. **User**: `myuser`
5. **Password**: `mypassword`

Run the following query:
```sql
SELECT * FROM users ORDER BY created_at DESC;
```

## Project Components

### `main.tf`

Defines the infrastructure using Terraform:
- **AWS Secrets Manager**: Stores the Postgres credentials as a single JSON object.
- **AWS Lambda**: Deploys the function using the `lambda.zip` file.
- **IAM**: Creates the necessary roles for the Lambda.

### `add_user_lambda/`

Contains the Lambda function logic:
- `models.py`: SQLAlchemy ORM models and secret retrieval logic.
- `lambda_handler.py`: Handler that retrieves secrets, **initializes the table**, and inserts a random user.

### `package_lambda.py`

A helper script that uses **Docker** to build a compatible Linux environment and package the `add_user_lambda/` folder along with its dependencies (SQLAlchemy, psycopg2) into a `lambda.zip` file.

## Configuration

All configuration, including database credentials and LocalStack endpoints, is managed in `terraform.tfvars`. Service configuration for Docker is managed directly in `docker-compose.yml`.

## Useful Commands

### Docker Commands

```bash
# Start container
docker compose up -d

# Stop container
docker compose down

# View logs
docker compose logs -f
```

### AWS CLI (LocalStack)

```bash
# List Lambda Functions
aws --endpoint-url=http://localhost:4566 lambda list-functions

# Check Secrets
aws --endpoint-url=http://localhost:4566 secretsmanager list-secrets
```

## Troubleshooting

### Connection Refused

If the Lambda cannot connect to Postgres, ensure `host.docker.internal` is reachable from within the LocalStack container. For older Docker versions on Linux, you might need to add it to `extra_hosts` in `docker-compose.yml`.

### Port Already in Use

If port 4566 or 5432 is already in use, modify the `docker-compose.yml` port mappings.

## Clean Up

To remove everything:

```bash
terraform destroy -auto-approve
docker compose down -v
rm lambda.zip response.json
```

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
