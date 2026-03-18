# Azure SQL Database + Azure Functions

Minimal viable example to work with **Azure SQL Edge** using **Azure Functions** and **SQLAlchemy**. This example demonstrates how to process HTTP POST requests and persist data into a SQL database.

## Project Structure

```
azure-sql-database/
├── .devcontainer/
│   └── devcontainer.json
├── functions/
│   └── register_user.py    # Function logic (Blueprint)
├── shared/
│   └── database.py         # SQLAlchemy models
├── sql/
│   └── init.sql            # DB initialization script
├── scripts/
│   ├── setup-mve.sh        # Setup environment
│   └── init-sql.sh         # Initialize SQL tables
├── .funcignore
├── function_app.py         # Azure Function entry point
├── host.json
├── local.settings.json
├── docker-compose.yml      # SQL Edge infrastructure
├── main.py                 # Test script (POST requester)
├── pyproject.toml
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (Recommended)
- Azure Functions Core Tools (Installed automatically in Dev Container)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` and select: **Dev Containers: Reopen in Container**
3. Wait for the container to build and dependencies to install

### Step 2: Run the Azure Function

Start the local Azure Functions runtime:

```bash
func start
```

### Step 3: Run the Example

In a new terminal, run the test script:

```bash
python main.py
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Setup Infrastructure

Start the SQL Edge container:

```bash
docker compose up -d
```

### Step 2: Setup Environment

Run the standardized setup script:

```bash
scripts/setup-mve.sh
```

### Step 3: Run the Function and Test

```bash
func start
# In another terminal
python main.py
```

## Validation

### Option A: VS Code SQL Server Extension

1. Install the **SQL Server (mssql)** extension.
2. Click the **SQL Server icon** on the activity bar.
3. Click **Add Connection (+)**.
4. Use the following details:
   - **Server name**: `azure-sql-edge`
   - **Authentication Type**: `SQL Login`
   - **User name**: `sa`
   - **Password**: `Password123!`
   - **Trust Server Certificate**: `True` (Essential for Local connection)
   - **Database**: `UserDB` (Created automatically during setup)

### Option B: Terminal (CURL)

You can verify the function directly using `curl`:

```bash
curl -X POST http://localhost:7071/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Smith", "email": "jane@example.com"}'
```

## Project Components

### Azure Function App (`function_app.py`)

- **Root Entrypoint**: Configures the FunctionApp and registers blueprints from the `functions/` directory.

### Function Logic (`functions/register_user.py`)

- **`register_user`**: HTTP Trigger (via Blueprint) that receives a JSON payload and uses the shared database layer to persist it.

### Database Layer (`shared/database.py`)

- **SQLAlchemy**: Centralized module for database models and connection logic using SQLAlchemy ORM.

## Clean Up

To remove containers and volumes:

```bash
docker compose down -v
```

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
