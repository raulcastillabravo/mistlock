# DevContainers with Docker Example

Minimal viable example to understand how DevContainers work with Docker, Python, and VS Code. This example demonstrates the key concepts and components of DevContainers through a simple pandas DataFrame application.

## What are DevContainers?

**DevContainers** (Development Containers) are a VS Code feature that allows you to use a Docker container as a complete development environment. Instead of installing dependencies, tools, and extensions on your local machine, everything runs inside a containerized environment.

### Key Benefits

- **Consistency**: Everyone on the team uses the exact same development environment
- **Isolation**: Project dependencies don't conflict with your local system
- **Reproducibility**: New team members can start coding in minutes
- **Portability**: Your development environment travels with your code

## Project Structure

```
devcontainers-docker/
├── .devcontainer/
│   └── devcontainer.json       # DevContainer configuration
├── .vscode/
│   └── settings.json           # VS Code settings
├── .env                        # Environment variables
├── main.py                     # Main Python script
├── pyproject.toml              # Python dependencies
├── uv.lock                     # Dependency lock file (auto-generated)
├── README.md                   # This file
└── README.es.md                # Spanish version
```

## Prerequisites

- **Docker** installed and running
- **VS Code** with the **Dev Containers** extension installed

## How to Use This Example

### Step 1: Open Project in Dev Container

1. Open VS Code in this project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

**What happens behind the scenes:**
- Docker pulls the Python base image
- The AWS CLI feature is installed
- The Git History extension is installed in the container
- The `postCreateCommand` runs to install dependencies with `uv`

### Step 2: Run the Example

Once inside the container, open a terminal and run:

```bash
python main.py
```

You should see output like:

```
Environment variable EXAMPLE_VAR: devcontainer-example

Creating a pandas DataFrame...

DataFrame created successfully!

DataFrame contents:
      Name  Age           City
0    Alice   25       New York
1      Bob   30  San Francisco
2  Charlie   35   Los Angeles
3    Diana   28        Chicago

DataFrame info:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   Name    4 non-null      object
 1   Age     4 non-null      int64 
 2   City    4 non-null      object
dtypes: int64(1), object(2)
memory usage: 224.0+ bytes
None

DataFrame statistics:
             Age
count   4.000000
mean   29.500000
std     4.203173
min    25.000000
25%    27.250000
50%    29.000000
75%    31.250000
max    35.000000
```

### Step 3: Verify AWS CLI Installation

The DevContainer includes the AWS CLI feature. Verify it's installed:

```bash
aws --version
```

You should see output like:

```
aws-cli/2.x.x Python/3.x.x Linux/x.x.x
```

### Step 4: Explore Git History Extension

The **Git History** extension is automatically installed in the container. You can:

1. Right-click on any file in VS Code
2. Select **Git: View File History**
3. Browse the commit history visually

## DevContainer Configuration Explained

### The `devcontainer.json` File

This is the heart of DevContainers. Let's break down each section:

```json
{
  "name": "DevContainers Python Example",
  "image": "mcr.microsoft.com/devcontainers/python:3.12-bookworm",
  "features": {
    "ghcr.io/devcontainers/features/aws-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "donjayamanne.githistory"
      ]
    }
  },
  "postCreateCommand": "pip3 install uv && uv sync"
}
```

#### 1. **`name`** - Container Name

```json
"name": "DevContainers Python Example"
```

The display name for your DevContainer. This appears in VS Code's status bar when you're connected to the container.

#### 2. **`image`** - Base Container Image

```json
"image": "mcr.microsoft.com/devcontainers/python:3.12-bookworm"
```

**What it does**: Specifies the Docker image to use as the base for your development environment.

**In this example**: We use Microsoft's official Python 3.12 DevContainer image based on Debian Bullseye.

**Alternatives**:
- Use a `Dockerfile` instead: `"dockerFile": "Dockerfile"`
- Use `docker-compose.yml`: `"dockerComposeFile": "docker-compose.yml"`

#### 3. **`features`** - Additional Tools and Capabilities

```json
"features": {
  "ghcr.io/devcontainers/features/aws-cli:1": {}
}
```

**What are features?**: Features are self-contained, shareable units of installation code that add tools, runtimes, or libraries to your DevContainer.

**In this example**: We install the AWS CLI feature, which adds the AWS command-line interface to our container.

**Popular features**:
- `ghcr.io/devcontainers/features/docker-outside-of-docker:1` - Docker CLI
- `ghcr.io/devcontainers/features/node:1` - Node.js
- `ghcr.io/devcontainers/features/git:1` - Git
- `ghcr.io/devcontainers/features/terraform:1` - Terraform

**Where to find features**: [https://containers.dev/features](https://containers.dev/features)

#### 4. **`customizations`** - VS Code Extensions

```json
"customizations": {
  "vscode": {
    "extensions": [
      "donjayamanne.githistory"
    ]
  }
}
```

**What it does**: Automatically installs VS Code extensions inside the DevContainer.

**In this example**: We install the **Git History** extension (`donjayamanne.githistory`), which provides a visual interface for viewing Git commit history.

**Why this matters**: Extensions installed in the container are isolated from your local VS Code installation. This ensures everyone on the team has the same development tools.

**How to find extension IDs**:
1. Open VS Code Extensions panel
2. Click on an extension
3. Look for the ID (e.g., `donjayamanne.githistory`)

#### 5. **`postCreateCommand`** - Post-Installation Script

```json
"postCreateCommand": "pip3 install uv && uv sync"
```

**What it does**: Runs a command after the container is created but before you start working.

**In this example**: 
1. `pip3 install uv` - Installs `uv`, a fast Python package installer
2. `uv sync` - Installs all dependencies from `pyproject.toml`

**Other use cases**:
- Install system packages: `"apt-get update && apt-get install -y git"`
- Run database migrations: `"python manage.py migrate"`
- Build the project: `"npm install && npm run build"`

**Alternatives**:
- `postStartCommand` - Runs every time the container starts
- `postAttachCommand` - Runs when you attach to the container
- `initializeCommand` - Runs on the host machine before container creation

## Python Dependencies with `uv`

### What is `uv`?

`uv` is a modern, fast Python package installer and resolver written in Rust. It's significantly faster than `pip` and provides better dependency resolution.

### The `pyproject.toml` File

```toml
[project]
name = "devcontainers-docker"
version = "0.1.0"
description = "Minimal viable example to understand DevContainers with Python and pandas"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "pandas",
    "python-dotenv",
]
```

**Key sections**:
- **`name`**: Project name
- **`dependencies`**: Python packages required for the project
- **`requires-python`**: Minimum Python version

### Managing Dependencies

```bash
# Install all dependencies
uv sync

# Add a new dependency
uv add numpy

# Update dependencies
uv lock --upgrade
```

## Main Script Explained

The `main.py` file demonstrates a simple pandas operation and environment variable loading:

```python
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Load environment variable
EXAMPLE_VAR = os.getenv("EXAMPLE_VAR", "default-value")

def main():
    print(f"Environment variable EXAMPLE_VAR: {EXAMPLE_VAR}\n")
    print("Creating a pandas DataFrame...")
    
    # Create a simple DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
    }
    
    df = pd.DataFrame(data)
    
    print("\nDataFrame created successfully!")
    print("\nDataFrame contents:")
    print(df)
```

**Purpose**: This simple script verifies that:
1. Python is working correctly
2. Dependencies (pandas, python-dotenv) are installed
3. Environment variables are loaded from `.env`
4. The development environment is fully functional

## Environment Variables

The `.env` file contains environment variables:

```
EXAMPLE_VAR=devcontainer-example
```

**Usage**: The `main.py` script loads this variable using `python-dotenv` and displays it at the start of execution. This demonstrates how to manage configuration through environment variables in your DevContainer projects.

## Useful Commands

### DevContainer Commands

```bash
# Rebuild container (if you change devcontainer.json)
# Press F1 → "Dev Containers: Rebuild Container"

# Close container and return to local
# Press F1 → "Dev Containers: Reopen Folder Locally"

# View container logs
# Press F1 → "Dev Containers: Show Container Log"
```

### Python Commands

```bash
# Run the main script
python main.py

# Install dependencies
uv sync

# Add a new package
uv add requests

# Check Python version
python --version
```

### AWS CLI Commands

```bash
# Check AWS CLI version
aws --version

# Configure AWS credentials (example)
aws configure

# List S3 buckets (if configured)
aws s3 ls
```

## How DevContainers Work: Under the Hood

1. **Container Creation**: When you open the project in a DevContainer, VS Code:
   - Reads `.devcontainer/devcontainer.json`
   - Pulls the specified Docker image
   - Creates a Docker container from that image

2. **Feature Installation**: VS Code installs any specified features (like AWS CLI) into the container

3. **Extension Installation**: VS Code installs the specified extensions inside the container

4. **Post-Create Command**: VS Code runs the `postCreateCommand` to set up dependencies

5. **Connection**: VS Code connects to the container and opens a remote session

6. **Development**: You code inside the container, but VS Code runs on your local machine

## Troubleshooting

### Container Won't Start

**Issue**: DevContainer fails to build or start.

**Solution**:
1. Check Docker is running: `docker ps`
2. View container logs: Press `F1` → "Dev Containers: Show Container Log"
3. Rebuild container: Press `F1` → "Dev Containers: Rebuild Container"

### Dependencies Not Installing

**Issue**: `postCreateCommand` fails or packages are missing.

**Solution**:
1. Manually run inside the container:
   ```bash
   pip3 install uv && uv sync
   ```
2. Check `pyproject.toml` for syntax errors

### Extension Not Working

**Issue**: Git History or other extensions don't appear.

**Solution**:
1. Check the extension ID is correct in `devcontainer.json`
2. Rebuild the container: Press `F1` → "Dev Containers: Rebuild Container"

### Port Already in Use

**Issue**: If you need to expose ports and they're already in use.

**Solution**: Add `forwardPorts` to `devcontainer.json`:
```json
"forwardPorts": [8000, 3000]
```

## Advanced DevContainer Features

### Running Docker Inside DevContainer

If you need Docker inside your DevContainer, add the Docker-in-Docker feature:

```json
"features": {
  "ghcr.io/devcontainers/features/docker-in-docker:1": {}
}
```

### Mounting Local Folders

To mount additional folders from your host machine:

```json
"mounts": [
  "source=/path/on/host,target=/path/in/container,type=bind"
]
```

### Environment Variables in DevContainer

Set environment variables directly in `devcontainer.json`:

```json
"containerEnv": {
  "MY_VARIABLE": "value"
}
```

### Using Docker Compose

For complex setups with multiple services:

```json
"dockerComposeFile": "docker-compose.yml",
"service": "app",
"workspaceFolder": "/workspace"
```

## Best Practices

1. **Keep it Simple**: Start with a basic configuration and add complexity as needed
2. **Document Features**: Explain why each feature or extension is needed
3. **Use Official Images**: Prefer Microsoft's DevContainer images for reliability
4. **Version Control**: Commit `.devcontainer/` to Git so everyone uses the same setup
5. **Test Regularly**: Rebuild containers periodically to catch issues early

## Next Steps

- Add more features (Node.js, Terraform, etc.)
- Create a custom Dockerfile for more control
- Use Docker Compose for multi-container setups
- Add database services (PostgreSQL, MongoDB, etc.)
- Implement automated testing in the DevContainer

## Resources

- **DevContainers Documentation**: [https://containers.dev/](https://containers.dev/)
- **VS Code DevContainers**: [https://code.visualstudio.com/docs/devcontainers/containers](https://code.visualstudio.com/docs/devcontainers/containers)
- **DevContainer Features**: [https://containers.dev/features](https://containers.dev/features)
- **DevContainer Images**: [https://github.com/devcontainers/images](https://github.com/devcontainers/images)

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
