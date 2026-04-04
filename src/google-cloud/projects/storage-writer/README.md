# Google Cloud Functions + Firebase Emulator Example

Minimal viable example to work with Google Cloud Functions locally using Firebase Emulator Suite and Python. This example demonstrates how to create an HTTP-triggered function that uploads files to Cloud Storage.

## Project Structure

```
gcp-functions/
├── functions/
│   ├── main.py
│   └── requirements.txt
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── firebase.json
├── .firebaserc
├── storage.rules
├── .env
├── test_function.py
├── pyproject.toml
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

The dev container includes:
- **Python 3.12** for test scripts
- **Node.js 18** for Firebase CLI
- **Java 17** required by Firebase Emulator Suite
- **Firebase Tools** (installed automatically)
- **VSFire extension** for Firebase integration

### Step 2: Set up Functions Virtual Environment

Firebase requires a virtual environment named `venv` inside the `functions` directory to load your code:

```bash
python3.12 -m venv functions/venv && functions/venv/bin/pip install -r functions/requirements.txt
```

### Step 3: Start Firebase Emulators

Inside the dev container terminal:

```bash
firebase emulators:start
```

You should see output like:

```
┌─────────────────────────────────────────────────────────────┐
│ ✔  All emulators ready! It is now safe to connect your app. │
│ i  View Emulator UI at http://localhost:4000                │
└─────────────────────────────────────────────────────────────┘

┌───────────┬────────────────┬─────────────────────────────────┐
│ Emulator  │ Host:Port      │ View in Emulator UI             │
├───────────┼────────────────┼─────────────────────────────────┤
│ Functions │ localhost:5001 │ http://localhost:4000/functions │
│ Storage   │ localhost:9199 │ http://localhost:4000/storage   │
└───────────┴────────────────┴─────────────────────────────────┘
```

### Step 4: View Emulator UI

Open your browser and navigate to:

```
http://localhost:4000
```

The Firebase Emulator UI provides:
- **Functions tab**: View deployed functions and their logs
- **Storage tab**: Browse uploaded files
- **Logs tab**: Real-time function execution logs

### Step 5: Test the Function

Open a new terminal (keep the emulator running) and execute:

```bash
python test_function.py
```

You should see output like:

```
Testing Firebase Cloud Function...
Function URL: http://localhost:5001/demo-project/us-central1/upload_file

Uploading 'test.txt'...
Status: 200
Response: File 'test.txt' uploaded to 'demo-bucket'

Check the Firebase Emulator UI at http://localhost:4000
```

### Step 6: Verify Upload in Emulator UI

1. Go to `http://localhost:4000`
2. Click on the **Storage** tab
3. You should see `demo-bucket` with `test.txt` inside
4. Click on **Functions** tab to see execution logs

### Step 7: Test with curl

You can also test the function directly with curl:

```bash
curl -X POST http://localhost:5001/demo-project/us-central1/upload_file \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "hello.txt",
    "content": "Hello from curl!"
  }'
```

Expected response:

```
File 'hello.txt' uploaded to 'demo-bucket'
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Prerequisites

**Install Node.js 18+:**
- Download from [nodejs.org](https://nodejs.org/)

**Install Java 17+:**
- Download from [adoptium.net](https://adoptium.net/)

**Install Firebase CLI:**

```bash
npm install -g firebase-tools
```

**Install Python Dependencies:**

```bash
pip3 install uv && uv sync
```

### Step 2: Set up Functions Virtual Environment

Firebase requires a virtual environment named `venv` inside the `functions` directory:

```bash
python3.12 -m venv functions/venv && functions/venv/bin/pip install -r functions/requirements.txt
```

### Step 3: Start Firebase Emulators

```bash
firebase emulators:start
```

You should see output like:

```
┌─────────────────────────────────────────────────────────────┐
│ ✔  All emulators ready! It is now safe to connect your app. │
│ i  View Emulator UI at http://localhost:4000                │
└─────────────────────────────────────────────────────────────┘

┌───────────┬────────────────┬─────────────────────────────────┐
│ Emulator  │ Host:Port      │ View in Emulator UI             │
├───────────┼────────────────┼─────────────────────────────────┤
│ Functions │ localhost:5001 │ http://localhost:4000/functions │
│ Storage   │ localhost:9199 │ http://localhost:4000/storage   │
└───────────┴────────────────┴─────────────────────────────────┘
```

### Step 4: Test the Function

Open a new terminal and run:

```bash
python test_function.py
```

## Project Components

### Cloud Function (`functions/main.py`)

HTTP-triggered Cloud Function that uploads files to Cloud Storage:

- **`@https_fn.on_request()`**: Decorator that defines an HTTP-triggered function
- **`upload_file(req)`**: Handler function that:
  - Validates the request method (POST only)
  - Extracts `filename` and `content` from JSON body
  - Uploads the content to Cloud Storage using `google-cloud-storage` client
  - Returns a success response (errors are handled by the framework)

### Function Dependencies (`functions/requirements.txt`)

Python packages required by the Cloud Function:

- **`firebase-functions`**: Firebase Functions SDK for Python
- **`google-cloud-storage`**: Google Cloud Storage client library

### Firebase Configuration (`firebase.json`)

Emulator configuration:

- **`functions.port`**: Port 5001 for Cloud Functions
- **`storage.port`**: Port 9199 for Cloud Storage
- **`ui.port`**: Port 4000 for Emulator UI
- **`functions.source`**: Points to `functions/` directory
- **`storage.rules`**: References security rules file

### Project Configuration (`.firebaserc`)

Defines the Firebase project ID for local emulation:

- **`projects.default`**: Set to `demo-project` for local development

### Storage Rules (`storage.rules`)

Security rules for Cloud Storage:

- Allows all read/write operations for local development
- In production, these should be restricted based on authentication

### Test Script (`test_function.py`)

Demonstration script that invokes the Cloud Function:

- Loads environment variables from `.env`
- Constructs the function URL using project ID and region
- Sends POST request with JSON payload
- Displays response and reminds to check Emulator UI

## Environment Variables

The `.env` file contains:

```
FIREBASE_PROJECT_ID=demo-project
STORAGE_BUCKET=demo-bucket
REGION=us-central1

# Emulator Endpoints
FUNCTIONS_EMULATOR_HOST=localhost:5001
STORAGE_EMULATOR_HOST=localhost:9199
FIRESTORE_EMULATOR_HOST=localhost:8080
```

**Note**: These are local development values. The emulator automatically uses these endpoints.

## Useful Commands

### Firebase CLI Commands

```bash
# Start all emulators
firebase emulators:start

# Start specific emulators
firebase emulators:start --only functions,storage

# Start with import/export data
firebase emulators:start --import=./emulator-data --export-on-exit

# View emulator status
firebase emulators:exec "echo 'Emulators running'"
```

### Testing Commands

```bash
# Run test script
python test_function.py

# Test with curl
curl -X POST http://localhost:5001/demo-project/us-central1/upload_file \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.txt", "content": "Hello!"}'
```

## Troubleshooting

### Port Already in Use

If ports 4000, 5001, or 9199 are already in use, modify `firebase.json`:

```json
{
  "emulators": {
    "functions": { "port": 5002 },
    "storage": { "port": 9200 },
    "ui": { "port": 4001 }
  }
}
```

Then update `.env` accordingly.

### Java Not Found

The Firebase Emulator Suite requires Java 17+. Install it:

**Ubuntu/Debian:**
```bash
sudo apt-get install openjdk-17-jdk
```

**macOS:**
```bash
brew install openjdk@17
```

**Windows:**
Download from [adoptium.net](https://adoptium.net/)

### Function Not Found

If the function doesn't appear:

1. Verify `functions/main.py` exists
2. Check `firebase.json` has correct `functions.source` path
3. Ensure `functions/requirements.txt` is present
4. Restart the emulator

### Import Errors in Function

If you get import errors when the function runs:

1. Check `functions/requirements.txt` includes all dependencies
2. The emulator automatically installs dependencies on first run
3. Delete `functions/__pycache__` and restart emulator

### Connection Refused

Make sure the emulator is running:

```bash
firebase emulators:start
```

Check the output for any errors during startup.

## Clean Up

To stop the emulators:

```bash
# Press Ctrl+C in the terminal running the emulator
```

To clear emulator data:

```bash
# Delete the emulator data directory
rm -rf .firebase
```

## Next Steps

- Add more trigger types (Pub/Sub, Firestore, Storage triggers)
- Implement authentication and authorization
- Add unit tests for functions
- Deploy to Google Cloud Functions
- Integrate with other Firebase services (Firestore, Auth)

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
