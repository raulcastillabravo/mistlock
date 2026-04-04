# AWS Step Functions + LocalStack Example

Minimal viable example to work with **AWS Step Functions** locally using **LocalStack**, **Python**, and **VS Code AWS Toolkit**. This example demonstrates a user onboarding workflow with parallel Lambda execution and IAM user creation.

## Project Structure

```
aws-step-functions/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── lambdas/
│   ├── log_user.py          # Writes to DynamoDB
│   └── validate_email.py    # Validates email format
├── deploy.py                # Infrastructure deployment script
├── docker-compose.yml       # LocalStack services
├── main.py                  # Workflow execution script
├── pyproject.toml
├── step_function.asl.json   # Step Function definition (ASL)
├── utils.py                 # Utilities for ZIP and config
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- [AWS Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-aws-us.aws-toolkit-vscode) (Included in Dev Container)
- [AWS CLI](https://aws.amazon.com/cli/) (Included in Dev Container)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Setup LocalStack Profile

Before running the example, configure a dedicated AWS profile for LocalStack:

```bash
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack
aws configure set endpoint_url http://localhost:4566 --profile localstack
```

### Step 3: Run the Example

1. Start LocalStack:
   ```bash
   docker compose up -d
   ```
2. Deploy infrastructure:
   ```bash
   python deploy.py
   ```
3. Run the workflow:
   ```bash
   python main.py
   ```

> **Note**: Wait **5-10 seconds** after `deploy.py` for LocalStack to finish initializing the Lambda environment before running `main.py`.

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Python Dependencies

```bash
pip3 install uv && uv sync
```

### Step 2: Setup LocalStack Profile

Configure the `localstack` profile as described in Option 1.

### Step 3: Run the Example

Follow the same steps as the Dev Container setup:
1. `docker compose up -d`
2. `python deploy.py`
3. `python main.py`

> **Note**: Wait **5-10 seconds** after `deploy.py` for LocalStack to finish initializing the Lambda environment.

## Project Components

### Infrastructure Script (`deploy.py`)

Handles the creation of all AWS resources:
- Creates the DynamoDB table for logging.
- Deploys Lambda functions using the `deploy_lambda` helper.
- Creates/Updates the Step Function state machine.

### Utilities (`utils.py`)

Shared helper functions:
- **`create_lambda_zip(path)`**: Generates a ZIP in memory for Lambda deployment.
- **`get_boto_config()`**: Returns the standard Boto3 configuration for LocalStack.
- **`deploy_lambda(client, name, ...)`**: Centralized logic to create/update Lambdas and inject environment variables.

### Main Script (`main.py`)

Demonstrates how to trigger and monitor the workflow:
1. Connects to Step Functions using the `localstack` endpoint.
2. Generates random user data.
3. Starts the execution and polls for completion.
4. Prints the final status and output.

### Step Function (`step_function.asl.json`)

The state machine definition using Amazon States Language (ASL):
- **ProcessUserOnboarding**: A `Parallel` state that runs both Lambdas simultaneously.
- **CreateIAMUser**: A `Task` using the AWS SDK integration to create a local IAM user if the previous steps succeed.

## Validation Steps

After running `main.py`, you can verify the results:

### 1. Verify IAM User Creation
```bash
aws iam list-users --profile localstack
```

### 2. Verify DynamoDB Logs
```bash
aws dynamodb scan --table-name UserLogs --profile localstack
```

### 3. Verify Lambda Functions
```bash
aws lambda list-functions --profile localstack
```

## Working with AWS Toolkit

This MVE is designed to showcase the ASL editor provided by the AWS Toolkit:

1. **Open Command Palette**: Press `F1` or `Ctrl+Shift+P`.
2. **Connect to AWS**: Type and select **AWS: Connect to AWS**.
3. **Select Profile**: Select the `localstack` profile.
4. **Render Graph**: Open `step_function.asl.json` and click the **Visual Graph** icon (top-right).
5. **Execute**: In the **AWS Explorer**, right-click `UserOnboardingWorkflow` and select **Start Execution**.

## Environment Variables

The `.env` file contains:

```
AWS_REGION=us-east-1
LOCALSTACK_ENDPOINT=http://localhost:4566
DYNAMODB_TABLE=UserLogs
STEP_FUNCTION_NAME=UserOnboardingWorkflow
```

## Useful Commands

### Docker Commands

```bash
# Start LocalStack
docker compose up -d

# Stop LocalStack
docker compose down

# View logs
docker compose logs -f localstack
```

### Manual Lambda Invocation (Testing)

You can invoke the Lambdas independently to test them:

**Test Email Validation:**
```bash
aws lambda invoke \
  --function-name ValidateEmailLambda \
  --payload '{"email": "valid@example.com"}' \
  --cli-binary-format raw-in-base64-out \
  --profile localstack \
  response.json
```

**Test User Logging:**
```bash
aws lambda invoke \
  --function-name LogUserLambda \
  --payload '{"username": "debug_user", "email": "debug@example.com"}' \
  --cli-binary-format raw-in-base64-out \
  --profile localstack \
  response.json
```

## Troubleshooting

### Lambda Function is 'Pending'

If you run `main.py` immediately after `deploy.py`, LocalStack might still be initializing the environment.

**Solution**: Wait 5-10 seconds and try again.

### Connection Refused

Make sure LocalStack is running:

```bash
docker ps
```

## Clean Up

To completely remove everything:

```bash
docker compose down -v
```

## Next Steps

- Add error handling to the Step Function (Catch/Retry).
- Implement a `Choice` state to branch logic based on email validation.
- Add unit tests for Lambda functions.

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
