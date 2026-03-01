# AWS Lambda

Minimal viable example of an **AWS Lambda** function that uploads files to **S3**. Built to run 100% locally using **LocalStack**.

## Architecture

```mermaid
architecture-beta
    group localstack(cloud)[AWS LocalStack]

    service lambda(server)[Lambda Function] in localstack
    service s3(disk)[S3 Bucket] in localstack

    lambda:R -- L:s3
```

[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Index

- [Quickstart (Dev Container)](#quickstart-dev-container)
- [Step by Step (without Dev Container)](#step-by-step-without-dev-container)
    - [1. Start infrastructure](#1-start-infrastructure)
    - [2. Configure AWS CLI](#2-configure-aws-cli)
    - [3. Install AWS Toolkit](#3-install-aws-toolkit)
    - [4. Install Python](#4-install-python)
    - [5. Deploy resources](#5-deploy-resources)
    - [6. Run the example](#6-run-the-example)
    - [7. Validation](#7-validation)
    - [8. Clean up](#8-clean-up)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Quickstart (Dev Container)

The Dev Container automatically provisions the LocalStack infrastructure and configures the Python environment and AWS CLI for immediate use.

1. **Prerequisites:**
    1. [Docker](https://www.docker.com/get-started) installed and running.
    2. [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed.

2. **Open project:** Open the **Command Palette** (`F1` or `Ctrl/Cmd+Shift+P`), also accessible via **View > Command Palette**, and select **Dev Containers: Reopen in Container**.
3. **Run MVE:** 
   ```bash
   python main.py
   ```
4. **Verify upload:**
   ```bash
   aws s3 ls s3://test-bucket/
   ```
5. **Clean up:**
   ```bash
   docker compose down -v
   ```

## Step by Step (without Dev Container)

This section details the steps performed automatically within the Dev Container, exploring additional variations and deployment options.

### 1. Start infrastructure

To start only the **LocalStack** service (avoiding the development container), run:

```bash
docker compose up -d localstack
```

### 2. Configure AWS CLI

Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configure a dedicated profile to point to your LocalStack instance:

```bash
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack
aws configure set endpoint_url http://localhost:4566 --profile localstack
aws configure set cli_pager "" --profile localstack
```

### 3. Install AWS Toolkit

Install the [AWS Toolkit](vscode:extension/amazonwebservices.aws-toolkit-vscode) extension. To use it with LocalStack:

1. Open the **AWS Toolkit** explorer in VS Code.
2. Click on the **Profiles** or **Connections** settings.
3. Select the `localstack` profile configured in step 2.

### 4. Install Python

Install [Python](https://www.python.org/downloads/) and verify the installation:

```bash
python --version
```

Then, install [uv](https://github.com/astral-sh/uv) and sync dependencies to create the virtual environment:

```bash
pip install uv
uv sync
```

### 5. Deploy resources

Before deploying, you must package the Lambda function:

```bash
python deploy/utils/package_lambda.py
```

Choose your preferred deployment option:

💡 **Note:** If you switch between different deployment methods (**Terraform**, **CloudFormation**, or **Boto3**), ensure you perform a **Clean Up** first to avoid resource name conflicts.

* **Option A**: Terraform

   ```bash
   terraform -chdir=deploy/terraform init
   terraform -chdir=deploy/terraform apply -auto-approve
   ```

* **Option B**: CloudFormation

   ```bash
   # 1. Create a temporary bucket for deployment
   aws s3 mb s3://lambda-deploy-bucket --profile localstack

   # 2. Upload the Lambda package
   aws s3 cp deploy/dist/function.zip s3://lambda-deploy-bucket/lambda.zip --profile localstack

   # 3. Deploy the stack
   aws cloudformation deploy --profile localstack \
     --stack-name aws-lambda-stack \
     --template-file deploy/cloudformation/template.yaml \
     --capabilities CAPABILITY_NAMED_IAM
   ```

   > 🎨 **Tip:** You can visualize this template using the **AWS Infrastructure Composer** from **AWS Toolkit** by opening `deploy/cloudformation/template.yaml` and clicking the "Infrastructure composer" button in the top-right corner of the editor.

* **Option C**: Boto3 (Python)

   ```bash
   python deploy/boto3/deploy.py
   ```

* <details><summary><b>Option D</b>: AWS CLI (Manual) - Click to expand</summary>

   ```bash
   # 1. Create IAM Role
   aws iam create-role --profile localstack \
     --role-name lambda-s3-role \
     --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

   # 2. Create Lambda Function
   aws lambda create-function --profile localstack \
     --function-name upload-to-s3 \
     --runtime python3.12 \
     --role arn:aws:iam::000000000000:role/lambda-s3-role \
     --handler lambda.lambda_handler \
     --zip-file fileb://deploy/dist/function.zip \
     --environment Variables={ENDPOINT_URL=http://localhost:4566}

   # 3. Create S3 Bucket
   aws s3 mb s3://test-bucket --profile localstack
   ```
</details>

### 6. Run the example

* **Option A**: Python Script. Run the demonstration script to invoke the Lambda and verify the upload:

   ```bash
   python main.py
   ```

* **Option B**: AWS Toolkit. You can browse resources and trigger the Lambda directly from the IDE:
    1. Select the `localstack` profile in the AWS Toolkit.
    2. To trigger the example, right-click on the `upload-to-s3` function and select **Invoke Lambda...**.

---

### 7. Validation

Choose your preferred way to verify the results:

* **Option A**: AWS CLI. Verify that the file was uploaded successfully:
    - **Check S3 Bucket**:
      ```bash
      aws s3 ls s3://test-bucket/ --profile localstack
      ```
    - **View Lambda Logs**:
      ```bash
      aws logs tail /aws/lambda/upload-to-s3 --profile localstack
      ```

* **Option B**: AWS Toolkit. Browse the resources directly from the VS Code sidebar:
    1. **S3**: Expand the S3 section to see the uploaded files.
    2. **CloudWatch**: Expand the Logs section to see the Lambda execution output.

---

### 8. Clean up

To completely remove the local infrastructure:

```bash
docker compose down -v
```

## Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Lambda Timeout** | Ensure LocalStack has enough memory/CPU resources. |
| **Connection Refused** | Ensure LocalStack is running and wait for the `Ready.` message in logs. |

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
