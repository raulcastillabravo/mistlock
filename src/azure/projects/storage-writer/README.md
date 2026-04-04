# Azure Functions + Azurite Example

Minimal viable example to work with Azure Functions locally using Azurite, Docker Compose, and Python. This example demonstrates how to create an HTTP-triggered function that uploads files to local blob storage.

## Project Structure

```
azure-functions/
├── upload-function/
│   ├── azurite_client.py
│   ├── function_app.py
│   ├── host.json
│   ├── local.settings.json
│   └── requirements.txt
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── docker-compose.yml
├── .env
├── main.py
├── pyproject.toml
├── README.es.md
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- Azure Functions Core Tools (installed automatically in dev container)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

The dev container includes:
- **Azure Functions extension** for local development and debugging
- **Azure Storage extension** for browsing blob storage
- **Azure CLI** for additional Azure operations

### Step 2: Start Azurite

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify it's running:

```bash
docker ps
```

### Step 3: Start Azure Functions

```bash
source .venv/bin/activate
func start --prefix ./upload-function/
```

You should see output like:

```
Azure Functions Core Tools
Core Tools Version:       4.x.x
Function Runtime Version: 4.x.x

Functions:

        UploadFile: [POST] http://localhost:7071/api/upload

For detailed output, run func with --verbose flag.
```

### Step 4: Test the Function

Open a new terminal and run:

```bash
python main.py
```

You should see:

```
Testing Azure Function upload endpoint...

Uploading 'test.txt'...
Status: 200
Response: File 'test.txt' uploaded to 'uploads'.
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Azure Functions Core Tools

Follow the official installation guide:
- **Windows**: `npm install -g azure-functions-core-tools@4 --unsafe-perm true`
- **macOS**: `brew tap azure/functions && brew install azure-functions-core-tools@4`
- **Linux**: Follow [official documentation](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)

### Step 2: Install Python Dependencies

```bash
pip3 install uv && uv sync
```

### Step 3: Start Azurite

Using Docker Compose:

```bash
docker compose up -d
```

### Step 4: Start Azure Functions

```bash
source .venv/bin/activate
func start --prefix ./upload-function/
```

### Step 5: Test the Function

```bash
python main.py
```

## Project Components

### AzuriteClient (`upload-function/azurite_client.py`)

Reusable client for Azurite blob storage operations:

- **`create_container(container_name)`**: Creates container if it doesn't exist
- **`upload_blob(container_name, blob_name, data)`**: Uploads data to blob

### Function App (`upload-function/function_app.py`)

Azure Functions application with HTTP trigger:

- **`@app.route`**: Defines HTTP endpoint `/api/upload` accepting POST requests
- **`upload_file(req)`**: Handles file upload using AzuriteClient
- **Error Handling**: Returns appropriate HTTP status codes

### Host Configuration (`upload-function/host.json`)

Global configuration for the Functions host:

- Logging settings
- Extension bundle configuration

### Local Settings (`upload-function/local.settings.json`)

Local development settings:

- **AzureWebJobsStorage**: Connection to Azurite for Functions runtime
- **AZURE_STORAGE_CONNECTION_STRING**: Connection for blob operations
- **BLOB_CONTAINER_NAME**: Target container for uploads

### Function Dependencies (`upload-function/requirements.txt`)

Python dependencies for Azure Functions runtime.

### Main Script (`main.py`)

Demonstration script that invokes the deployed Azure Function:

- Makes HTTP POST request to the function endpoint
- Uploads a test file
- Displays the response

### Docker Compose (`docker-compose.yml`)

Azurite service configuration:

- Blob service on port 10000
- Queue service on port 10001
- Table service on port 10002

## Environment Variables

The `.env` file contains:

```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;

BLOB_CONTAINER_NAME=uploads
```

**Note**: The connection string uses Azurite's default credentials for local development.

## Azure Functions Extension

The **Azure Functions** VS Code extension (included in the dev container) provides:

- **Local Debugging**: Set breakpoints and debug functions locally
- **Function Management**: Create, delete, and manage functions from VS Code
- **Deployment**: Deploy functions to Azure directly from the editor
- **Log Streaming**: View real-time logs from your functions

### Using the Extension

1. Open the Azure view in VS Code (Azure icon in the sidebar)
2. Under "Workspace", you'll see your local functions
3. Right-click on a function to debug, test, or view logs
4. Use the "Execute Function Now" option to test without external calls

## Useful Commands

### Azure Functions Commands

```bash
# Start Functions runtime
cd upload-function
func start

# Start with verbose logging
func start --verbose

# Create a new function
func new

# Install extensions
func extensions install
```

### Docker Commands

```bash
# Start Azurite container
docker compose up -d

# Stop container
docker compose down

# Stop and remove volumes (delete all data)
docker compose down -v

# View logs
docker compose logs -f azurite
```

### Testing Commands

```bash
# Run the test script
python main.py

# Or use curl directly
curl -X POST "http://localhost:7071/api/upload?filename=test.txt" \
  -H "Content-Type: text/plain" \
  -d "Hello from Azure Functions!"
```

## Troubleshooting

### Port Already in Use

If port 7071 (Functions) or 10000 (Azurite) is already in use:

**For Azurite**, modify `docker-compose.yml`:

```yaml
ports:
  - "10010:10000"
```

Then update connection strings in `.env` and `upload-function/local.settings.json`:

```
BlobEndpoint=http://127.0.0.1:10010/devstoreaccount1
```

**For Functions**, set a different port:

```bash
func start --port 7072
```

### Connection Refused

Make sure Azurite is running:

```bash
docker ps
```

Check the connection string in `upload-function/local.settings.json` matches your Azurite configuration.

### Module Not Found

If you get import errors in the function:

```bash
cd upload-function
pip install -r requirements.txt
```

### Function Not Found

If the function doesn't appear when running `func start`:

1. Verify you're in the `upload-function` directory
2. Check that `function_app.py` exists
3. Verify `host.json` has the correct extension bundle
4. Try deleting `.venv` and reinstalling dependencies

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the Azurite image (optional)
docker rmi mcr.microsoft.com/azure-storage/azurite
```

## Next Steps

- Add more trigger types (Timer, Queue, Blob)
- Implement function bindings for automatic blob operations
- Add unit tests for functions
- Deploy to Azure Functions in the cloud
- Add authentication and authorization

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
