# Redis

Minimal viable example to work with **Redis** using **Python** and **Docker**. This example demonstrates how to manage user status (Enum) using Redis and a custom context manager for connection management.

## Architecture

```mermaid
architecture-beta
    group api(cloud)[Cloud]
    
    service app(server)[Python Script] in api
    service db(database)[Redis] in api
    
    db:L <--> R:app
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

- [Docker](https://www.docker.com/get-started) installed and running.
- [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed.

## Quickstart

1. **Open in Container**: Open VS Code in the project folder and select **Dev Containers: Reopen in Container** from the Command Palette (`F1`).
2. **Run the Example**:
   ```bash
   python main.py
   ```

💡 **Next Steps**: See the [How to debug](#how-to-debug), [How to test](#how-to-test), [Validate results](#validate-results) and [Clean Up](#clean-up) sections below.

## Setup Environment

If you are not using a Dev Container, you can set up the environment manually:

```bash
scripts/setup.sh
```

## Start Infrastructure

Launch the required containers:
```bash
docker compose up -d
```

## How to execute

### Using python

Execute the demonstration script:
```bash
python main.py
```

## How to debug

### The main.py client

1. Open `main.py`.
2. Set breakpoints in the code.
3. Press `F5` to start debugging.

## How to test

### Individually

You can run tests individually from the VS Code **Testing** tab.

### All tests

To execution all tests (unit and integration) using the automated script:

```bash
scripts/run_tests.sh
```

## Validate results

Verify that the user status is correctly stored in Redis.

1. **Check using Redis CLI**: Use the custom script that connects to the container:
   ```bash
   scripts/redis_cli.sh GET raulcastillabravo:status
   ```
2. **Check using Redis Insight**: Connect to the database and browse keys to see `raulcastillabravo:status`.

### Connection Details
- **Server**: `localhost`
- **Port**: `6379`
- **Password**: `redis123`

## Clean Up

To stop all services and remove the state:
```bash
docker compose down -v
```
