# MinIO + Boto3 + Docker Example

Minimal viable example to work with MinIO using Docker Compose, Boto3 (AWS SDK for Python), and pandas for data manipulation.

## Project Structure

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── minio_client.py
├── pyproject.toml
├── main.py
├── uv.lock
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- MinIO Console access (browser-based)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Start MinIO Container

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify it's running:

```bash
docker ps
```

### Step 3: Create Bucket

Before running the script, create the bucket in the MinIO Console:
1. Open [http://localhost:9001](http://localhost:9001) (User/Pass: `minioadmin`).
2. Go to **Buckets** > **Create Bucket** and name it `test-bucket`.

### Step 4: Run the Example

```bash
python main.py
```

You should see output like:

```
Bucket 'test-bucket' created successfully.
Created dummy DataFrame:
   id  value category
0   1     10        A
1   2     20        B
2   3     30        A
3   4     40        B
4   5     50        C
Saved DataFrame to 'data.csv'.
File 'data.csv' uploaded to 'test-bucket/data.csv'.
File 'test-bucket/data.csv' downloaded to 'downloaded_data.csv'.
Downloaded DataFrame:
   id  value category
0   1     10        A
1   2     20        B
2   3     30        A
3   4     40        B
4   5     50        C
Local files cleaned up.
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Python Dependencies

```bash
pip3 install uv && uv sync
```

### Step 2: Start MinIO Container

```bash
docker compose up -d
```

### Step 3: Create Bucket

1. Open [http://localhost:9001](http://localhost:9001) (User/Pass: `minioadmin`).
2. Go to **Buckets** > **Create Bucket** and name it `test-bucket`.

### Step 4: Run the Example

```bash
python main.py
```

## Accessing MinIO Console

### Step 1: Open Console in Browser

1. Navigate to: [http://localhost:9001](http://localhost:9001)
2. Enter credentials:
   - **Username:** `minioadmin`
   - **Password:** `minioadmin`

### Step 2: View Buckets and Files

1. In the MinIO Console, click on **Buckets** in the left sidebar
2. You should see the `test-bucket` bucket
3. Click on `test-bucket` to view its contents
4. You should see the `data.csv` file uploaded by the Python script
5. You can download, preview, or manage files through the console

## MinIO Client API

The `minio_client.py` module provides a simple wrapper around boto3 for common MinIO operations:

### Available Methods

| Method           | Description                                      | Parameters                                    |
|------------------|--------------------------------------------------|-----------------------------------------------|
| `create_bucket`  | Creates a new bucket if it doesn't exist         | `bucket_name` (str)                           |
| `upload_file`    | Uploads a file to a bucket                       | `file_name` (str), `bucket` (str), `object_name` (str, optional) |
| `download_file`  | Downloads a file from a bucket                   | `bucket` (str), `object_name` (str), `file_name` (str) |
| `delete_file`    | Deletes a file from a bucket                     | `bucket` (str), `object_name` (str)           |

### Example Usage

```python
from minio_client import MinioClient

# Initialize client
client = MinioClient()

# Create bucket
client.create_bucket("my-bucket")

# Upload file
client.upload_file("local_file.csv", "my-bucket", "remote_file.csv")

# Download file
client.download_file("my-bucket", "remote_file.csv", "downloaded_file.csv")

# Delete file
client.delete_file("my-bucket", "remote_file.csv")
```

## Environment Variables

The `.env` file contains:

```
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=http://localhost:9000
BUCKET_NAME=test-bucket
```

You can modify these values as needed. Remember to recreate the containers if you change MinIO credentials.

## Useful Commands

### Docker Commands

```bash
# Start containers
docker compose up -d

# Stop containers
docker compose down

# Stop and remove volumes (delete all data)
docker compose down -v

# View logs
docker compose logs -f

# View only MinIO logs
docker compose logs -f minio
```

## Troubleshooting

### Port Already in Use

If ports 9000 or 9001 are already in use, modify the `docker-compose.yml` ports section:

```yaml
ports:
  - "9002:9000"  # API port
  - "9003:9001"  # Console port
```

Then update `MINIO_ENDPOINT` in `.env`:

```
MINIO_ENDPOINT=http://localhost:9002
```

And restart:

```bash
docker compose down
docker compose up -d
```

### Connection Refused

Make sure the MinIO container is running:

```bash
docker ps
```

Check the logs for errors:

```bash
docker compose logs minio
```

### Module Not Found

If you get import errors, install dependencies:

```bash
pip3 install uv && uv sync
```

### Permission Denied (Dev Container)

If you get permission errors with Docker in the dev container, make sure the `docker-outside-of-docker` feature is properly configured in `devcontainer.json`.

### Cannot Access MinIO Console

If you cannot access the console at `http://localhost:9001`:

1. Check that the container is running: `docker ps`
2. Verify the port mapping is correct: `docker compose ps`
3. Try accessing via `http://127.0.0.1:9001`
4. Check firewall settings

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the MinIO image (optional)
docker rmi minio/minio
```

## Next Steps

- Implement bucket policies for access control
- Add versioning to buckets
- Implement object lifecycle management
- Add encryption for sensitive data
- Create API endpoints with FastAPI to expose MinIO operations
- Implement file streaming for large files
- Add unit tests for MinIO client operations

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
