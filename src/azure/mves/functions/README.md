# Azure Functions

This MVE demonstrates how to develop and test Azure Functions locally using the **Azure Functions Core Tools**.

## Architecture

```mermaid
architecture-beta
    group cloud(cloud)[Azure]

    service func(server)[Functions Emulator] in cloud
    service client(internet)[Python Client]

    client -- "HTTP GET/POST" --> func
```

[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

- **Python Client**: A simple script that sends HTTP requests to the function.
- **Functions Emulator**: Local runtime provided by Azure Functions Core Tools.

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
- [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers)

## Quickstart

1. **Open in Container**: Open VS Code in this folder and select **Dev Containers: Reopen in Container**.
2. **Run the Example**: `python main.py`.

## Setup Environment

If you are not using a Dev Container, you can set up the environment manually: `scripts/setup.sh`

## Start Infrastructure

If you are not using a Dev Container, launch the required services: `docker compose up -d`

## How to execute

1. **Using python**:
    - **Interactive**: `python main.py`
    - **Script**: `scripts/run_main.sh`
2. **Using curl**:
    - **Run**: `curl "http://localhost:7071/api/get_secret?username=admin"`
3. **Using REST Client**:
    - **Open**: `app.http` (if created) or use any REST client.

## How to debug

1. **main.py**:
    - **Open**: `main.py`
    - **Breakpoints**: Set a breakpoint in the `main` function.
    - **Run**: Press `F5` or use the "Run and Debug" tab.
2. **Functions**:
    - **Open**: `function_app.py`
    - **Breakpoints**: Set a breakpoint inside `get_secret`.
    - **Run**: Use the Azure Functions VS Code extension or attach the debugger to the `func host start` process.

## How to test

1. **Individually**: Via VS Code Testing tab.
2. **All tests**: Via automated script (`scripts/run_tests.sh`).

## Validate results

1. **Check using Terminal**:
    - **Verify**: The output of `main.py` should show the secret for 'admin' and 403 for other users.
2. **Check using Logs**:
    - **Inspect**: Review the output of the terminal running `func start` to see the function execution logs.

## Clean Up

`docker compose down -v`
