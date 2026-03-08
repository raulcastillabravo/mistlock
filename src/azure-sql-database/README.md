# Azure SQL Database with Dapr

Minimal viable example demonstrating an event-driven flow: processing a CSV file uploaded to Azurite (Azure Blob Storage) and inserting the records into Azure SQL Edge using Dapr bindings.

## Architecture

```mermaid
architecture-beta
    service blob_sender(internet)[Upload CSV]
    group azurite_group(cloud)[Local Emulation]
        service azurite(disk)[Azurite Blob]
        service sql_edge(database)[Azure SQL Edge]
    group dapr_group(server)[Event Flow]
        service dapr(server)[Dapr Sidecar]
        service app(server)[FastAPI App]

    blob_sender:R -- L:azurite
    azurite:R -- L:daprd
    daprd:R -- L:app
    app:L -- R:daprd
    daprd:L -- R:sql_edge
```
[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Index
- [Quickstart (Dev Container)](#quickstart-dev-container)
- [Step by Step (Local Setup)](#step-by-step-local-setup)
- [Project Components](#project-components)
- [Validation](#validation)
- [Clean Up](#clean-up)

---

## Quickstart (Dev Container)

**Prerequisites**: [Docker](https://www.docker.com/get-started) and [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers).

1. Press `F1` and select: **Dev Containers: Reopen in Container**.
2. Run `docker compose up -d`.
3. Wait for SQL initialization: `scripts/init-sql.sh`.
4. Upload a CSV to Azurite and check the SQL table.
5. Clean up: `docker compose down -v`.

---

## Step by Step (Local Setup)

### 1. Start Infrastructure
Start all services including Dapr and SQL:
```bash
docker compose up -d
```

### 2. Setup Environment
Install dependencies and tools with the standardized setup script:
```bash
scripts/setup-mve.sh
```

### 3. Initialize SQL Tables
The SQL table must be created once SQL Edge is running:
```bash
scripts/init-sql.sh
```

### 4. Run the Example
The application is already running inside the `app` container via Docker Compose. You can monitor logs to verify connectivity:
```bash
docker compose logs -f app
```

### 5. Validation
Upload a sample CSV named `sample_users.csv`.

**Sample Content (`sample.csv`):**
```csv
name,email
Alice,alice@example.com
Bob,bob@example.com
```

**Upload to Azurite:**
You can use any storage explorer or standard curl if you have the container created:
```bash
# Upload sample data to the 'inbound' container
curl -X PUT -H "x-ms-blob-type: BlockBlob" \
     --data-binary @sample.csv \
     "http://localhost:10000/devstoreaccount1/inbound/sample.csv"
```

**Query SQL Edge:**
Verify the data was inserted:
```bash
docker exec -it sql_local /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P Password123! \
  -Q "SELECT * FROM users"
```

---

## Project Components

### FastAPI App (`main.py`)
- **`process_blob`**: Triggered by Dapr when a new blob arrives. It parses the CSV rows and uses the Dapr Client to call the SQL Binding.

### Dapr Components (`dapr/components/`)
- **`blob-input.yaml`**: Monitors the `inbound` container in Azurite.
- **`sql-output.yaml`**: Connects to Azure SQL Edge to execute `INSERT` statements.

---

## Clean Up
Remove all services and volumes:
```bash
docker compose down -v
```

## License
This is a minimal example for educational purposes. Feel free to use and modify as needed.
