# GCP Cloud SQL (PostgreSQL) + Firebase Local Emulator

Minimal viable example to work with **Google Cloud SQL (PostgreSQL)** emulated locally using **Docker Compose**, and **Firebase Cloud Functions** triggered by **Cloud Storage**. This example demonstrates a full data pipeline: CSV Upload -> Storage Trigger -> Function Processing -> Postgres Insertion.

## Project Structure

```
gcp-cloud-sql/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── functions/
│   ├── main.py              # Cloud Function (V2) logic
│   └── requirements.txt     # Function dependencies
├── scripts/
│   └── setup-mve.sh         # Standardized setup script
├── docker-compose.yml       # PostgreSQL container
├── .env                     # Local connection strings
├── firebase.json            # Emulator config
├── mise.toml                # Tool configuration
├── main.py                  # Main demo script
├── pyproject.toml           # Project dependencies
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P`
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the environment to build. It will install all required tools (**Node.js**, **Java**, **Firebase Tools**, **mise**, **uv**) and Python dependencies automatically.

### Step 2: Start Services

Open a terminal inside the Dev Container and run:

```bash
# Start PostgreSQL
docker compose up -d

# Start Firebase Emulators
firebase emulators:start
```

### Step 3: Run the Example

Open a second terminal and execute:

```bash
python main.py
```

You should see output like:
```
🚀 Starting demo...
✅ CSV uploaded to storage emulator.
⏳ Waiting for Cloud Function... (1s)
📊 Found 2 records in Postgres:
 - Antigravity (anti@gravity.ai)
 - User (user@example.com)
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Start Infrastructure

```bash
docker compose up -d
```

### Step 2: Setup Environment

Instead of manual configuration, use our standardized setup script. This script automatically installs **mise** and **uv**, installs required tool versions (**Python**, **Node.js**, **Java**), installs **firebase-tools**, and syncs all dependencies.

```bash
scripts/setup-mve.sh
```

### Step 3: Start Emulators

```bash
firebase emulators:start
```

### Step 4: Run the Example

```bash
python main.py
```

## Project Components

### Cloud Function (`functions/main.py`)

A Storage-triggered function that:
- Trigger: `on_object_finalized` (file upload).
- Mechanism: Downloads CSV, parses it, and uses **SQLAlchemy ORM** to save to PostgreSQL.

### Main Script (`main.py`)

- Uploads a sample `users.csv` to the Storage emulator.
- Polls the PostgreSQL database using **SQLAlchemy** until the new records are detected.

## Environment Variables

The `.env` file contains:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mve_db
STORAGE_BUCKET=mve-gcp-cloud-sql.appspot.com
FIREBASE_STORAGE_EMULATOR_HOST="localhost:9199"
GCP_PROJECT=mve-gcp-cloud-sql
```

## Clean Up

To completely remove the local infrastructure (containers and volumes):

```bash
docker compose down -v
```

## Next Steps

- Integrate more GCP services.
- Add unit tests for the Cloud Function.

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
