# Minimal Viable Examples (MVE)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raulcastillabravo/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/raulcastillabravo/mve-collection/blob/main/LICENSE)

This repository teaches how to develop for the Cloud for free, without an account and without a credit card, emulating AWS, Azure, and Google Cloud locally:

* ✅ **Free and account-less**: All technologies are free and do not require creating an account anywhere.
* **💯% compatible**: The code you develop locally is 100% compatible with the real Cloud.
* 📦 **Self-contained**: Each example is independent and includes everything necessary to run it.
* 🚀 **Ready to run**: Examples are ready to run without making code changes.
* 🐳 **Dockerized**: All have dockerized development environments.
* 🖥️ **Graphical interfaces**: Use of graphical tools to manage the local Cloud environment.
* 📖 **Well documented**: All examples are documented in English and Spanish.

> ⭐ **If you find this repository useful, please consider giving it a star!** It helps other developers find these examples and supports further development.

## 🚀 Quick Start

1. **Prerequisites:**
    1. [Docker](https://www.docker.com/get-started) installed and running.
    2. [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed.

2. **Open an example:** Open an example folder (e.g., `src/aws-dynamo-db`) in VS Code.
3. **Reopen in Container:** Open the **Command Palette** (`F1` or `Ctrl/Cmd+Shift+P`) and select **Dev Containers: Reopen in Container**.
4. **Follow instructions:** Once the container is ready, follow the instructions in the example's `README.md`. Usually, it's just:
   ```bash
   python main.py
   ```

## 📚 Available Examples

Some examples appear multiple times because they integrate several cloud services.

### 🟠 AWS (Amazon Web Services)

| Service | MVE | Description |
| :--- | :--- | :--- |
| **S3** | [aws-lambda](./src/aws-lambda/) | Deploys a Lambda function that uploads objects to S3, emulated with LocalStack, Terraform, CloudFormation, and Boto3. |
| **S3** | [aws-s3](./src/aws-s3/) | Emulates S3 locally using Garage to implement a data pipeline with Boto3, PyArrow, and Delta Lake. |
| **S3** | [aws-dynamo-db](./src/aws-dynamo-db/) | Demonstrates a file processing pipeline where S3 uploads trigger a Lambda to log metadata into a DynamoDB table, all emulated with LocalStack, Terraform, and CloudFormation. |
| **Dynamo DB** | [aws-dynamo-db](./src/aws-dynamo-db/) | Demonstrates a file processing pipeline where S3 uploads trigger a Lambda to log metadata into a DynamoDB table, all emulated with LocalStack, Terraform, and CloudFormation. |
| **Dynamo DB** | [aws-step-functions](./src/aws-step-functions/) | Orchestrates a user onboarding workflow with AWS Step Functions that executes parallel Lambdas and logs results to DynamoDB, using LocalStack and the AWS Toolkit. |
| **RDS (Postgres)** | [localstack-hybrid-cloud](./src/localstack-hybrid-cloud/) | Demonstrates a hybrid cloud scenario where an AWS Lambda (simulated in LocalStack) retrieves credentials from Secrets Manager via Terraform to interact with an external PostgreSQL database. |
| **Lambda** | [aws-lambda](./src/aws-lambda/) | Deploys a Lambda function that uploads objects to S3, emulated with LocalStack, Terraform, CloudFormation, and Boto3. |
| **Lambda** | [aws-dynamo-db](./src/aws-dynamo-db/) | Demonstrates a file processing pipeline where S3 uploads trigger a Lambda to log metadata into a DynamoDB table, all emulated with LocalStack, Terraform, and CloudFormation. |
| **Lambda** | [aws-step-functions](./src/aws-step-functions/) | Orchestrates a user onboarding workflow with AWS Step Functions that executes parallel Lambdas and logs results to DynamoDB, using LocalStack and the AWS Toolkit. |
| **Step Functions** | [aws-step-functions](./src/aws-step-functions/) | Orchestrates a user onboarding workflow with AWS Step Functions that executes parallel Lambdas and logs results to DynamoDB, using LocalStack and the AWS Toolkit. |

### 🔵 Microsoft Azure

| Service | MVE | Description |
| :--- | :--- | :--- |
| **Blob Storage** | [azurite-docker](./src/azurite-docker/) | Implements local Azure Blob Storage operations like creating containers and uploading/downloading blobs using Azurite and Python. |
| **Blob Storage** | [azure-functions](./src/azure-functions/) | Creates an HTTP-triggered Azure Function that uploads files to local blob storage emulated by Azurite, using Python and Docker Compose. |
| **Cosmos DB** | [azure-cosmos-db](./src/azure-cosmos-db/) | Integrates a Python application with the Azure Cosmos DB Emulator running in Docker to perform basic database operations locally. |
| **Azure SQL** | [azure-sql-database](./src/azure-sql-database/) | Inserts user data into Azure SQL Edge via a Python HTTP-triggered Azure Function using SQLAlchemy. |
| **Azure Functions** | [azure-functions](./src/azure-functions/) | Creates an HTTP-triggered Azure Function that uploads files to local blob storage emulated by Azurite, using Python and Docker Compose. |
| **Azure Functions** | [azure-sql-database](./src/azure-sql-database/) | Inserts user data into Azure SQL Edge via a Python HTTP-triggered Azure Function using SQLAlchemy. |
| **Databricks** | [databricks-docker](./src/databricks-docker/) | Simulates a high-fidelity Databricks environment (Runtime 15.4 LTS) using Docker, MinIO for S3 storage, and PostgreSQL for the Hive Metastore to test Spark and Delta Lake ETLs. |

### 🔴 GCP (Google Cloud Platform)

| Service | MVE | Description |
| :--- | :--- | :--- |
| **Cloud Storage** | [gcp-functions](./src/gcp-functions/) | Implements an HTTP-triggered Google Cloud Function that uploads files to Cloud Storage using the Firebase Emulator Suite for local development. |
| **Cloud Storage** | [gcp-cloud-sql](./src/gcp-cloud-sql/) | Processes CSV files uploaded to Cloud Storage using a triggered Cloud Function that inserts the data into a local PostgreSQL database. |
| **Firestore** | [gcp-cloud-run](./src/gcp-cloud-run/) | Deploys a containerized Google Cloud Run service that registers patient data in Firestore using the Firebase Emulator Suite and Python. |
| **Cloud Functions** | [gcp-functions](./src/gcp-functions/) | Implements an HTTP-triggered Google Cloud Function that uploads files to Cloud Storage using the Firebase Emulator Suite for local development. |
| **Cloud Functions** | [gcp-cloud-sql](./src/gcp-cloud-sql/) | Processes CSV files uploaded to Cloud Storage using a triggered Cloud Function that inserts the data into a local PostgreSQL database. |
| **Cloud Run** | [gcp-cloud-run](./src/gcp-cloud-run/) | Deploys a containerized Google Cloud Run service that registers patient data in Firestore using the Firebase Emulator Suite and Python. |
| **Cloud SQL (Postgres)** | [gcp-cloud-sql](./src/gcp-cloud-sql/) | Processes CSV files uploaded to Cloud Storage using a triggered Cloud Function that inserts the data into a local PostgreSQL database. |

### 🟢 Hybrid & Others

| Service | MVE | Description |
| :--- | :--- | :--- |
| **MinIO** | [minio-docker-boto3](./src/minio-docker-boto3/) | Demonstrates S3-compatible object storage operations using MinIO, the Boto3 SDK, and pandas to manage CSV files locally. |
| **MinIO** | [minio-docker-delta](./src/minio-docker-delta/) | Implements ACID transactions and time travel capabilities on MinIO using Delta Lake (delta-rs) and Python for reliable local data storage. |
| **Mongo** | [mongo-docker-mongoengine](./src/mongo-docker-mongoengine/) | Integrates Python with MongoDB using the MongoEngine ODM and Docker Compose for local NoSQL database development. |
| **Postgres** | [postgres-docker](./src/postgres-docker/) | Sets up a PostgreSQL database with SQLAlchemy ORM and Docker Compose for standard relational database development and testing. |
| **Postgres** | [localstack-hybrid-cloud](./src/localstack-hybrid-cloud/) | Demonstrates interaction with an external PostgreSQL database from an AWS environment simulated in LocalStack. |
| **Redis** | [redis-docker](./src/redis-docker/) | Implements basic Redis operations using the Python redis client and Docker for local caching and data structure storage. |
| **Redis** | [redis-docker-mutex](./src/redis-docker-mutex/) | Implements a distributed mutex (lock) using Redis to coordinate access to shared resources across multiple processes or threads. |
| **Metabase** | [metabase-docker](./src/metabase-docker/) | Sets up Metabase for data visualization and BI, connected to a local PostgreSQL database with sample data generated via SQLAlchemy. |
| **RabbitMQ** | [rabbitmq-docker-pika](./src/rabbitmq-docker-pika/) | Implements a publish-subscribe messaging pattern using RabbitMQ, the pika client, and Python for asynchronous event processing. |
| **Airflow** | [airflow-docker](./src/airflow-docker/) | Deploys a complete Apache Airflow environment with Docker to run and monitor a Python-based ETL pipeline using pandas. |
| **Dev Containers** | [devcontainers-docker](./src/devcontainers-docker/) | Explains the core concepts of VS Code Dev Containers through a simple pandas application, showcasing environment isolation and pre-configured tools. |

_More examples coming soon..._

## 📝 License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
