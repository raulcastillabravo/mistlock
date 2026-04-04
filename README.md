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
    2. (Optional, but recommended) [VS Code](https://code.visualstudio.com/) with [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed.

2. **Open an example:** Open an example folder (e.g., `src/aws/mves/s3-garage/`) in VS Code.
3. **Reopen in Container:** Open the **Command Palette** (`F1` or `Ctrl/Cmd+Shift+P`) and select **Dev Containers: Reopen in Container**.
4. **Follow instructions:** Once the container is ready, follow the instructions in the example's `README.md`. Usually, it's just:
   ```bash
   python main.py
   ```

## 📚 Available Examples

There are two types of examples:

*   **MVE (Minimal Viable Example)**: Defines everything needed to emulate a specific Cloud service and the tools required to develop with it locally.
*   **Project**: Shows how to combine different Cloud services (MVEs) to develop a specific use case. You can see the services used in each project between parentheses in the table below.

### 🟠 AWS (Amazon Web Services)

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **S3** | • [s3-garage](./src/aws/mves/s3-garage/)<br>• [s3-minio-boto3](./src/aws/mves/s3-minio-boto3/)<br>• [s3-minio-delta](./src/aws/mves/s3-minio-delta/) | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **Dynamo DB** | • *(coming soon)* | • [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB) |
| **Lambda** | • *(coming soon)* | • [storage-writer](./src/aws/projects/storage-writer/) (Lambda → S3)<br>• [simple-etl](./src/aws/projects/simple-etl/) (S3 → Lambda → DynamoDB)<br>• [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **Step Functions** | • [step-functions-localstack](./src/aws/mves/step-functions-localstack/) | • *(coming soon)* |
| **RDS (Postgres)** | • [rds-postgres (Postgres)](./src/hybrid/mves/postgres/) | • [sql-writer](./src/aws/projects/sql-writer/) (Lambda → Postgres) |
| **ElastiCache (Redis)** | • [elasti-cache (Redis)](./src/hybrid/mves/redis/) | • *(coming soon)* |


### 🔵 Microsoft Azure

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **Blob Storage** | • [blob-storage](./src/azure/mves/blob-storage/) | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage) |
| **Cosmos DB** | • *(coming soon)* | • [no-sql-writer](./src/azure/projects/no-sql-writer/) (Python → Cosmos DB) |
| **Azure SQL** | • *(coming soon)* | • [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Azure Functions** | • *(coming soon)* | • [storage-writer](./src/azure/projects/storage-writer/) (Azure Function → Blob Storage)<br>• [sql-writer](./src/azure/projects/sql-writer/) (Azure Function → Azure SQL) |
| **Databricks** | • [databricks](./src/azure/mves/databricks/) | • *(coming soon)* |
| **Cache for Redis** | • [cache-for-redis (Redis)](./src/hybrid/mves/redis/) | • *(coming soon)* |


### 🔴 GCP (Google Cloud Platform)

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **Cloud Storage** | • *(coming soon)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Firestore** | • *(coming soon)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Cloud Functions** | • *(coming soon)* | • [storage-writer](./src/google-cloud/projects/storage-writer/) (Cloud Function → Cloud Storage)<br>• [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Cloud Run** | • *(coming soon)* | • [no-sql-writer](./src/google-cloud/projects/no-sql-writer/) (Cloud Run → Firestore) |
| **Cloud SQL** | • [cloud-sql (Postgres)](./src/hybrid/mves/postgres/) | • [simple-etl](./src/google-cloud/projects/simple-etl/) (Storage → Cloud Function → Postgres) |
| **Memorystore (Redis)** | • [memorystore (Redis)](./src/hybrid/mves/redis/) | • *(coming soon)* |


### 🟢 Hybrid & Others

| Service | MVE | Projects |
| :--- | :--- | :--- |
| **Airflow** | • [airflow](./src/hybrid/mves/airflow/) | • *(coming soon)* |
| **Dev Containers** | • [devcontainers](./src/hybrid/mves/devcontainers/) | • *(coming soon)* |
| **Metabase** | • [metabase](./src/hybrid/mves/metabase/) | • *(coming soon)* |
| **Mongo** | • [mongo](./src/hybrid/mves/mongo/) | • *(coming soon)* |
| **Postgres** | • [postgres](./src/hybrid/mves/postgres/) | • *(coming soon)* |
| **RabbitMQ** | • [rabbitmq](./src/hybrid/mves/rabbitmq/) | • *(coming soon)* |
| **Redis** | • [redis](./src/hybrid/mves/redis/) | • [redis-mutex](./src/hybrid/projects/redis-mutex/) (Python → Redis) |


_More examples coming soon..._

## 📝 License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
