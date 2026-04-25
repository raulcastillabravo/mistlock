# MongoDB

Minimal Viable Example for MongoDB using Docker Compose, MongoEngine ODM, and MongoDB Compass for validation.

## Architecture

```mermaid
architecture-beta
    group api(cloud)[API Layer]
    group db(database)[Database Layer]

    service python(server)[Python App] in api
    service mongo(database)[MongoDB] in db

    python:R -- L:mongo
```
[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Index

- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Setup Environment](#setup-environment)
- [Start Infrastructure](#start-infrastructure)
- [How to execute](#how-to-execute)
- [How to debug](#how-to-debug)
- [How to test](#how-to-test)
- [Validate results](#validate-results)
- [Clean Up](#clean-up)

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) (Recommended)
- [MongoDB Compass](https://www.mongodb.com/try/download/compass) (Optional, for validation)

## Quickstart

1. Open in Container.
2. Execute `python main.py`.

## Setup Environment

If not using Dev Containers, run the setup script:

```bash
bash scripts/setup.sh
```

## Start Infrastructure

Launch the MongoDB service:

```bash
docker compose up -d
```

## How to execute

### Using python

Run the example script:

```bash
bash scripts/run_main.sh
```

### Using mongosh

Access the MongoDB shell and copy-paste the content of `playgrounds/users.mongodb.js`:

1. Run `./scripts/mongosh.sh`.
2. Copy and paste the script from `playgrounds/users.mongodb.js`.

### Using VS Code Playground

1. Open `playgrounds/users.mongodb.js`.
2. Click the **Play** icon in the top right of the editor.

### Using MongoDB Compass

1. Connect to MongoDB using Compass.
2. Navigate to `my_db` -> `users`.
3. Click **Add Data** -> **Insert Document** to create a user manually.
4. Alternatively, use the **embedded Mongosh** at the bottom to run the playground script.

## How to debug

### The main.py client

1. Open `main.py`.
2. Press `F5` and select **Python: Main**.

## How to test

### Individually

Use the VS Code Testing side bar to run tests.

### All tests

Run the automated test script:

```bash
bash scripts/run_tests.sh
```

## Validate results

### Using MongoDB Compass (Recommended)

1. [Download and install MongoDB Compass](https://www.mongodb.com/try/download/compass).
2. Create a new connection with this string:
   ```
   mongodb://admin:admin123@localhost:27017/my_db?authSource=admin&uuidRepresentation=standard
   ```
3. Navigate to `my_db` -> `users` to see the documents.

### Using mongosh

You can also verify the data directly from the terminal:
1. Run `./scripts/mongosh.sh`.
2. Execute the following query:
   ```javascript
   db.getSiblingDB('my_db').users.find().pretty()
   ```

### Using VS Code Extension

The Dev Container includes the **MongoDB for VS Code** extension.
1. Open the MongoDB icon in the activity bar.
2. Add a new connection using the same connection string.
3. You can use **Playgrounds** to run interactive queries.

## Clean Up

Stop services and remove volumes:

```bash
docker compose down -v
```
