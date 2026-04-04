# Databricks Local Environment with Docker

Minimal viable example to simulate a Databricks environment locally using Docker, **MinIO as S3 compatible storage, and PostgreSQL as a persistent Hive Metastore**. This example demonstrates how to develop and test Spark/Delta Lake ETLs locally with a high degree of fidelity to the cloud environment by using **Databricks Runtime 15.4 LTS (Spark 3.5.0)**.

## Project Structure

```
databricks-docker/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── src/
│   ├── databricks_shim/
│   │   ├── connect.py
│   │   └── utils.py
│   └── notebooks/
│       └── analysis.ipynb
├── Dockerfile
├── docker-compose.yml
├── .env
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Run the Example

```bash
python main.py
```

You should see output indicating the transformation from Bronze to Silver layers and a final verification query.

### Step 3: Interactive Analysis

Open `src/notebooks/analysis.ipynb` and run the cells to analyze the data registered in the Hive Metastore and **test the DBUtils Shim** (secrets and widgets).
> **Note**: This interactive feature is only available when using the **Dev Container** as it provides the pre-configured Jupyter environment.

## Option 2: Local Setup (Without Dev Container)

### Step 1: Start Infrastructure

```bash
docker compose up -d
```

This will start:
- **Spark**: Standalone Spark instance.
- **MinIO**: S3-compatible storage.
- **Postgres**: Backend for the Hive Metastore.
- **mc**: Utility to automatically create the `BUCKET_NAME` defined in `.env`.

### Step 2: Run the Example

Execute the script directly inside the Spark container:

```bash
docker compose exec spark python3 main.py
```

## Project Components

### Spark Client (`src/databricks_shim/connect.py`)

Function `get_spark_session(app_name)`:

- **Environment Detection**: Uses the `APP_ENV` variable to switch between Local and Cloud modes.
- **Emulation**: Configures S3A connectors, Delta Lake extensions, and Hive Metastore JDBC connection when `APP_ENV=local`.

### Databricks Shim (`src/databricks_shim/utils.py`)

Partial mock for `dbutils`:

- **Secrets**: `dbutils.secrets.get()` maps to environment variables.
- **Widgets**: `dbutils.widgets.get()` maps to environment variables.
- **Testing**: The `analysis.ipynb` notebook includes a section to verify these mocks.
- **Extensibility**: Designed to be expanded with more `fs` or `notebook` methods as needed.

### Main Script (`main.py`)

ETL Demonstration:

- 1. Generates raw data with an explicit schema.
- 2. Saves data to the **Bronze** layer (Delta Lake in MinIO).
- 3. Reads Bronze, transforms it, and saves it to the **Silver** layer as a **Managed Table** in the Hive Metastore.

## Environment Variables

The `.env` file contains critical configurations:

```
BUCKET_NAME=demo-bucket
STORAGE_PREFIX=s3a
AWS_ENDPOINT_URL=http://minio:9000
POSTGRES_HOST=postgres
```

**Note**: `STORAGE_PREFIX` allows high portability. You can change it to `abfss` when moving to Azure without changing the logic.

## Useful Commands

### Docker Commands

```bash
# Start environment
docker compose up -d

# View Spark/Metastore logs
docker compose logs -f

# Completely stop and clean
docker compose down -v
```

## Troubleshooting

### Connection Refused

Ensure all services are running:

```bash
docker compose ps
```

### Table already exists

If you run the ETL multiple times with different schemas, you may encounter Metastore conflicts. Use `spark.sql("DROP TABLE IF EXISTS sales.products_silver")` or clean the volumes.

## Clean Up

To remove containers and persistent data:

```bash
docker compose down -v
```

## Next Steps

- Implement Delta Lake Time Travel tests.
- Add more `dbutils.fs` mock methods.
- Integrate with local BI tools connecting to the Hive Metastore.

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
