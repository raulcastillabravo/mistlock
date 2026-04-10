# Minimal Viable Examples (MVE)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raulcastillabravo/)

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
    2. (Optional, but recommended) [VS Code](https://code.visualstudio.com/) with [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed.

2. **Open an example:** Open an example folder (e.g., `src/aws/mves/s3-garage/`) in VS Code.
3. **Reopen in Container:** Open the **Command Palette** (`F1` or `Ctrl/Cmd+Shift+P`) and select **Dev Containers: Reopen in Container**.
4. **Follow instructions:** Once the container is ready, follow the instructions in the example's `README.md`. Usually, it's just:
   ```bash
   python main.py
   ```

## 📚 Available Examples

There are two types of examples:

*   **MVE (Minimal Viable Example)**: Focus on one specific Cloud service, how to emulate it and which tools are required to develop with it locally. There can be more than one MVE per service if there are several tools to emulate it.
*   **Project**: Combine different Cloud services in the same local development environment. You can see the services used in each project between parentheses in the table below.

### 🟠 AWS (Amazon Web Services)

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **Lambda** | • *(coming soon)* | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB)<br>• [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **ECS / EKS** | • *(coming soon)* | |
| **Glue** | • *(coming soon)* | |
| **S3** | • [s3-garage](./src/aws/mves/s3-garage/)<br>• [s3-minio-boto3](./src/aws/mves/s3-minio-boto3/)<br>• [s3-minio-delta](./src/aws/mves/s3-minio-delta/) | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **RDS (Postgres)** | • [rds-postgres (Postgres)](./src/hybrid/mves/postgres/) | • [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **Dynamo DB** | • *(coming soon)* | • [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **ElastiCache (Redis)** | • [elasti-cache (Redis)](./src/hybrid/mves/redis/) | |
| **Step Functions** | • [step-functions-localstack](./src/aws/mves/step-functions-localstack/) | |
| **SQS / SNS** | • *(coming soon)* | |
| **EventBridge** | • *(coming soon)* | |
| **CloudFormation** | • *(coming soon)* | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |


### 🔵 Microsoft Azure

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **Azure Functions** | • *(coming soon)* | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage)<br>• [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Container Apps** | • *(coming soon)* | |
| **Databricks** | • [databricks](./src/azure/mves/databricks/) | |
| **Blob Storage** | • [blob-storage](./src/azure/mves/blob-storage/) | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage) |
| **Azure SQL** | • *(coming soon)* | • [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Cosmos DB** | • *(coming soon)* | • [no-sql-writer](./src/azure/projects/no-sql-writer/) (Python → Cosmos DB) |
| **Cache for Redis** | • [cache-for-redis (Redis)](./src/hybrid/mves/redis/) | |
| **Service Bus** | • *(coming soon)* | |
| **Event Grid** | • *(coming soon)* | |


### 🔴 GCP (Google Cloud Platform)

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **Cloud Functions** | • [firebase-functions](./src/google-cloud/mves/firebase-functions/) | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Cloud Run** | • *(coming soon)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Dataflow** | • *(coming soon)* | |
| **Cloud Storage** | • *(coming soon)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Cloud SQL** | • [cloud-sql (Postgres)](./src/hybrid/mves/postgres/) | • [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Firestore** | • *(coming soon)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Memorystore** | • [memorystore (Redis)](./src/hybrid/mves/redis/) | |
| **Pub/Sub** | • *(coming soon)* | |


### 🟢 Hybrid & Others

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **MinIO** | • [s3-minio-boto3](./src/aws/mves/s3-minio-boto3/)<br>• [s3-minio-delta](./src/aws/mves/s3-minio-delta/) | |
| **Postgres** | • [postgres](./src/hybrid/mves/postgres/) | |
| **MongoDB** | • [mongo](./src/hybrid/mves/mongo/) | |
| **Redis** | • [redis](./src/hybrid/mves/redis/) | • [redis-mutex](./src/hybrid/projects/redis-mutex/) (Python → Redis) |
| **Airflow** | • [airflow](./src/hybrid/mves/airflow/) | |
| **RabbitMQ** | • [rabbitmq](./src/hybrid/mves/rabbitmq/) | |
| **Terraform** | • *(coming soon)* | • [storage-writer (AWS)](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl (AWS)](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB)<br>• [sql-writer (AWS)](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **Metabase** | • [metabase](./src/hybrid/mves/metabase/) | |
| **Dev Containers** | • [devcontainers](./src/hybrid/mves/devcontainers/) | |

## 🚀 Roadmap
- [ ] Add one MVE for each service in the table above.
  <details>
  <summary>See next steps</summary>

  - 2026-04-20
    - [x] MVE Google Functions (Firebase).
    - [ ] MVE Azure Functions.
    - [ ] MVE AWS Lambda using SAM Framework.
  - Next batch:
    - [ ] MVE Google Dataflow.
    - [ ] MVE Azure Cosmos DB.
    - [ ] MVE AWS Glue.
  - Backlog:
    - [ ] MVE AWS Lambda con MiniStack.
    - [ ] MVE AWS ECS / EKS.
    - [ ] MVE AWS S3 con RustFS.
    - [ ] MVE AWS DynamoDB Official Image.
    - [ ] MVE AWS Step Functions Official Image.
    - [ ] MVE AWS SQS / SNS.
    - [ ] MVE AWS Eventbridge.
    - [ ] MVE AWS CloudFormation.
    - [ ] Merge MinIO MVEs in one.
    - [ ] MVE Azure Container Apps (ACA).
    - [ ] MVE Azure SQL Edge.
    - [ ] MVE Azure Service Bus.
    - [ ] MVE Azure Event Grid.
    - [ ] MVE Google Cloud Run.
    - [ ] MVE Google Firebase Storage.
    - [ ] MVE Google Firebase Firestore.
    - [ ] MVE Google Firebase Pub/Sub.
    - [ ] MVE Terraform.
  </details>
- [ ] Add tests and unify the structure of all MVEs and projects to follow the same pattern.
- [ ] Create a GitHub Pages with repository documentation.
- [ ] Record videos with explanations and demos for each MVE.

## 📝 Author's Note

This project is the foundation of the **educational content** that I generate on social media (and my largest Open Source project to date 😄).

It is completely free and open to the community; use it to **learn and practice with total freedom**.

I only hope that it is of great use to you and that you support it so that other developers also know about it. It is the engine that allows me to continue creating **content and training for the community**.

