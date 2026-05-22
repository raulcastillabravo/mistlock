---
isLab: true
title: S3 Garage
description: Minimal viable example to work with AWS S3 using Garage as a local emulator. This example demonstrates a data pipeline using Boto3, PyArrow, and Delta Lake (...
---

# AWS S3

Minimal viable example to work with **AWS S3** using **Garage** as a local emulator. This example demonstrates a data pipeline using **Boto3**, **PyArrow**, and **Delta Lake** (delta-rs).

## Architecture

```mermaid
architecture-beta
    group local(cloud)[AWS]
    
    service garage(disk)[Garage S3] in local
    service app(server)[Python App] in local
    
    garage:L -- R:app
```

[![View Diagram](https://img.shields.io/badge/View_Diagram-Install-blue?logo=visualstudiocode)](vscode:extension/mermaidchart.vscode-mermaid-chart)

## Index

- [Quickstart (Dev Container)](#quickstart-dev-container)
- [Step by Step (without Dev Container)](#step-by-step-without-dev-container)
- [Validation](#validation)
- [Clean Up](#clean-up)
- [Troubleshooting](#troubleshooting)

## Quickstart (Dev Container)

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed.
- [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) installed.

### Steps

1. **Open in Container**: Open VS Code in the project folder and select **Dev Containers: Reopen in Container** from the Command Palette (`F1`).

   ℹ️ **Note**: Garage S3 connection keys are automatically refreshed when starting or restarting the development environment. Use the ones generated in your `.env`, not the ones from the repository.

2. **Run the Example**:
   ```bash
   python main.py
   ```

💡 **Next Steps**: See the [Validation](#validation) and [Clean Up](#clean-up) sections below.

## Step by Step (without Dev Container)

### 1. Start Infrastructure
Launch the required containers:
```bash
docker compose up -d
```

### 2. Setup Environment
Install dependencies and system tools using mise:
```bash
scripts/setup.sh
```

ℹ️ **Note**: Garage S3 connection keys are automatically refreshed when starting or restarting the development environment. Use the ones generated in your `.env`, not the ones from the repository.

### 3. Run Example
Execute the demonstration script:
```bash
python main.py
```

## Validation

Explain how to verify the example is working correctly.

1. **Check Buckets**: Verify that `bronze` and `silver` buckets were created.
   ```bash
   aws s3 ls --profile garage
   ```
2. **Check Content**: Verify the files in the silver bucket.
   ```bash
   aws s3 ls s3://silver --recursive --profile garage
   ```
3. **Explore with Rclone (GUI)**:
   Launch the Rclone graphical interface to explore the files visually:
   ```bash
   scripts/rclone-gui.sh
   ```
   Navigate to `http://127.0.0.1:5572` in your browser.

## Clean Up

To stop all services and remove the state:
```bash
docker compose down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Garage API not ready | Ensure the `garage` container is running and wait a few seconds for the API to initialize. Check logs with `docker logs garage`. |
| Port 3900 in use | Stop any other service using port 3900 or change the mapping in `docker-compose.yml`. |

