# Google Cloud Run + Firebase Emulator Example

Minimal viable example to work with Google Cloud Run locally using Firebase Emulator Suite and Python. This example demonstrates how to create a containerized service that registers patients in Firestore.

## Project Structure

```
gcp-cloud-run/
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── firebase.json
├── .firebaserc
├── firestore.rules
├── .env
├── main.py
├── pyproject.toml
└── README.md
```

## Prerequisites

- **Docker and Docker Compose** installed
- **VS Code**

## Option 1: Using Dev Container (Fast & Simple)

> **⚠️ LIMITATIONS:** This option uses **Docker** directly to run the service. It does **NOT** use Cloud Code or Minikube.
> - **Pros**: Fast setup, no complex configuration, works immediately.
> - **Cons**: No "Hot Reload" (requires rebuild on change), no real infrastructure simulation (YAML configuration, Knative behavior), no integrated debugging.
> - **Recommended for**: Quick testing of code logic and Firestore integration.
> 
> **For a full professional environment with Minikube/Cloud Code, see Option 2.**

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder.
2. Press `F1` -> **Dev Containers: Reopen in Container**.

The container includes Python, Node.js, Java, and Firebase Tools.

### Step 2: Start Firebase Emulators

Inside the dev container terminal:

```bash
firebase emulators:start
```

### Step 3: Run the Service (Docker)

Open a **new terminal** inside VS Code:

```bash
# Build the image
docker build -t patient-service ./app

# Run the container (network=host to access Firebase Emulator)
docker run --rm -p 8080:8080 --net=host -e FIRESTORE_EMULATOR_HOST=localhost:8081 patient-service
```

### Step 4: Test the Service

Open a **third terminal**:

**Option A: Using Python script**

```bash
python main.py
```

**Option B: Using curl**

```bash
curl -v -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"name": "Test", "surname": "User", "dni": "12345678X"}'
```

---

## Option 2: Local Setup (Professional / Cloud Code)

This option mimics the real Cloud environment using **Minikube** and **Cloud Code**. Ideal for deep development.

### Step 1: Install Prerequisites

Even though Cloud Code can attempt to install dependencies, **manual installation is recommended** for stability.

#### Linux (Debian/Ubuntu)
Ensure `curl` is installed:
```bash
sudo apt-get install -y curl
```

1. **Python (Min v3.12)**:
   ```bash
   sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
   ```

2. **Node.js v24**: [Install Guide](https://nodesource.com/products/distributions)
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Java JDK v21**: [Download (Oracle)](https://www.oracle.com/java/technologies/downloads/)
   ```bash
   sudo apt-get update && sudo apt-get install -y openjdk-21-jdk
   ```

4. **Google Cloud CLI**: [Install Guide](https://cloud.google.com/sdk/docs/install)
   ```bash
   sudo apt-get install -y apt-transport-https ca-certificates gnupg curl
   curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
   echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
   sudo apt-get update && sudo apt-get install -y google-cloud-cli google-cloud-cli-skaffold
   ```

5. **Minikube**: [Install Guide](https://minikube.sigs.k8s.io/docs/start/)
   ```bash
   curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
   ```

6. **Firebase CLI**:
   ```bash
   sudo npm install -g firebase-tools
   ```

#### Windows
1. **Python (Min v3.12)**: [Download](https://www.python.org/downloads/)
2. **Node.js (Min v18)**: [Download](https://nodejs.org/en/download/)
3. **Java JDK (Min v17)**: [Download (Oracle)](https://www.oracle.com/java/technologies/downloads/)
4. **Google Cloud CLI**: [Install Guide](https://cloud.google.com/sdk/docs/install)
5. **Minikube**:
   ```powershell
   winget install Kubernetes.minikube
   ```
6. **Firebase CLI**:
   ```powershell
   npm install -g firebase-tools
   ```

#### macOS
1. **Python (Min v3.12)**: [Download](https://www.python.org/downloads/)
2. **Node.js (Min v18)**: [Download](https://nodejs.org/en/download/)
3. **Java JDK (Min v17)**: [Download (Oracle)](https://www.oracle.com/java/technologies/downloads/)
4. **Google Cloud CLI**: [Install Guide](https://cloud.google.com/sdk/docs/install)
5. **Minikube**:
   ```bash
   brew install minikube
   ```
6. **Firebase CLI**:
   ```bash
   sudo npm install -g firebase-tools
   ```

7. **Install VS Code Extension**: Search for "Google Cloud Code" in VS Code and install it.

### Step 2: Setup Project

1. **Install Python Dependencies**:
   It is recommended to use the standalone installer for `uv` to avoid system conflicts.

   **Linux/macOS**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   uv sync
   ```

   **Windows**:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   uv sync
   ```

### Step 3: Start Emulators

```bash
firebase emulators:start
```

### Step 4: Run with Cloud Code

This project pre-configures `cloudcode.useGcloudAuthSkaffold: false` in `.vscode/settings.json` to avoid mandatory Google Cloud login prompts and ensure a 100% offline experience. If prompted for Google authentication anyway, select **No/Cancel**; this MVE can be run 100% locally.

1. Click on the **Cloud Code** icon in VS Code activity bar.
2. Expand **Cloud Run**.
3. Click the **Run on Cloud Run Emulator** (play icon).
   - > **Initialization**: The first time you run this, Cloud Code needs to download and set up **Minikube**. This can take **10-15 minutes** (one-time process).
   - Cloud Code will use `skaffold` to build and deploy to your local Minikube.
   - **Hot Reload** is active: save a file, and it updates automatically.

### Step 5: Test

> **Linux Users**: If connection fails with `Connection refused`, change `FIRESTORE_EMULATOR_HOST` in `.vscode/launch.json` to `host.minikube.internal:8081`. The default `host.docker.internal` is optimized for Windows/WSL/macOS.

**Option A: Using Python script**

```bash
python main.py
```

**Option B: Using curl**

```bash
curl -v -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"name": "Test", "surname": "User", "dni": "12345678X"}'
```

## Project Components

### Cloud Run Service (`app/main.py`)
Flask app that receives patient data and writes to Firestore. Auto-detects emulator via `FIRESTORE_EMULATOR_HOST`.

### Dockerfile (`app/Dockerfile`)
Production-grade container using `gunicorn`.

### Firestore Rules (`firestore.rules`)
Permissive rules for local development.

## Environment Variables

The `.env` file contains:

```
GCP_PROJECT_ID=demo-project
SERVICE_URL=http://localhost
FIRESTORE_EMULATOR_HOST=localhost:8081
SERVICE_PORT=8080
```

## Useful Commands

```bash
# Stop containers
docker system prune

# Stop Minikube
minikube stop
```

## Troubleshooting

### Connection Refused (111)

If the Cloud Run service fails to connect to Firestore with a `Connection refused` error:
- Ensure the Firebase Emulator is running (`firebase emulators:start`).
- Check if Firestore is listening on `0.0.0.0` in `firebase.json`.
- In `.vscode/launch.json`, try changing `FIRESTORE_EMULATOR_HOST` to `host.minikube.internal:8081` (Native Linux) or your local IP.

### Persistent Google Cloud Login Prompts

If VS Code keeps asking you to log in to Google Cloud:
- Ensure `.vscode/settings.json` includes `"cloudcode.useGcloudAuthSkaffold": false`.
- Select "No" or "Cancel" when prompted; the MVE works 100% locally.

### Firebase Emulator Fails to Start

- Ensure **Node.js** and **Java (JDK)** are installed.
- Check if another process is using ports `8081` or `4000`.

## Clean Up

### Stopping Local Services

To stop the resources used in this MVE:

```bash
# Option 1: Stop the specific Docker container
docker stop patient-service 2>/dev/null || true

# Option 2: Cloud Code deployment is stopped by clicking "Stop" (Red Square) in VS Code.
# Alternatively, you can stop Minikube:
minikube stop

# Stop Firebase Emulators
pkill -f firebase
```
### Uninstalling Prerequisites (Optional)

If you wish to completely remove the installed tools:

#### Linux (Debian/Ubuntu)
```bash
# Remove Node.js
sudo apt-get purge -y nodejs && sudo apt-get autoremove -y

# Remove Java (JDK 21)
sudo apt-get purge -y openjdk-21-jdk && sudo apt-get autoremove -y

# Remove Minikube
sudo rm /usr/local/bin/minikube
```

#### Windows / macOS
1.  **Google Cloud CLI / Firebase**: Use the system's "Uninstall a program" or "Applications" folder.
2.  **Minikube / Node / Java**: Use the official uninstaller for each tool or the "Add/Remove Programs" section in Windows Settings.

## Next Steps

- Add more endpoints
- Implement Authentication using Firebase Auth Emulator
- Add unit tests for the Flask application

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
