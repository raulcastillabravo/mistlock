# MinIO + Delta Lake + Docker Example

Minimal viable example to work with MinIO using Docker Compose and Delta Lake (delta-rs) for ACID transactions and time travel capabilities.

## Project Structure

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── minio_delta.py
├── pyproject.toml
├── main.py
├── uv.lock
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- MinIO Console access (optional)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Start MinIO Service

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify the service is running:

```bash
docker ps
```

You should see the `minio_delta` container.

### Step 3: Create MinIO Bucket

1. Open your browser and go to: **http://localhost:9001**
2. Login with:
   - **Username:** `minioadmin`
   - **Password:** `minioadmin`
3. Click on **Buckets** in the left sidebar
4. Click **Create Bucket** button
5. Enter bucket name: `delta-bucket`
6. Click **Create Bucket**

### Step 4: Run the Example Script

```bash
python main.py
```

You should see output showing:
- Writing partitioned Delta table by category
- Reading all data from the table
- Overwriting only the Electronics partition using predicate
- Reading all data to verify Accessories partition remains unchanged

### Step 5: View Data in MinIO Console (Optional)

1. Go back to the MinIO Console: **http://localhost:9001**
2. Navigate to **Buckets** → `delta-bucket` → `sales_data/`
3. You'll see the Delta Lake directory structure with Parquet files and transaction logs

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Python Dependencies

```bash
pip3 install uv && uv sync
```

### Step 2: Start MinIO Service

```bash
docker compose up -d
```

### Step 3: Create MinIO Bucket

Follow Step 3 from Option 1 above.

### Step 4: Run the Example

```bash
python main.py
```

### Step 5: View Data in MinIO Console

Follow Step 5 from Option 1 above.

## What is Delta Lake?

Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark and big data workloads. Key features:

- **ACID Transactions**: Ensures data integrity
- **Time Travel**: Access previous versions of data
- **Schema Evolution**: Modify table schemas over time
- **Unified Batch and Streaming**: Single table for both operations
- **Audit History**: Complete history of all changes

## How the Example Works

The `MinioDelta` class provides two main methods:

1. **`write(df, path, mode="overwrite", partition_by=None, predicate=None)`**: Write pandas DataFrame as Delta table
   - `df`: pandas DataFrame to write
   - `path`: Table path within the bucket
   - `mode`: Write mode (`overwrite`, `append`, `error`, `ignore`)
   - `partition_by`: Optional list of columns to partition by
   - `predicate`: Optional SQL predicate to filter which data to overwrite (e.g., `"category = 'Electronics'"`)
   - Creates Delta Lake transaction log and stores data in Parquet format

2. **`read(path, columns=None, filters=None)`**: Read Delta table into pandas DataFrame
   - `path`: Table path within the bucket
   - `columns`: Optional list of columns to read
   - `filters`: Optional list of filters (e.g., `[("category", "=", "Electronics")]`)
   - Returns latest version as pandas DataFrame

### Example Usage

```python
client = MinioDelta()

# Write with partitioning
client.write(df, "sales_data", partition_by=["category"])

# Read with filtering
electronics = client.read("sales_data", filters=[("category", "=", "Electronics")])

# Overwrite only a specific partition using predicate
client.write(
    updated_data, 
    "sales_data", 
    mode="overwrite",
    predicate="category = 'Electronics'"
)
```

### Important Storage Options for MinIO

The `MinioDelta` class uses the following critical storage options for MinIO compatibility:

```python
{
    "AWS_ALLOW_HTTP": "true",  # Enable HTTP connections (required for local MinIO)
    "aws_conditional_put": "etag",  # Enable atomic operations using ETags
}
```

These options are essential for Delta Lake to work correctly with MinIO.

## Environment Variables

The `.env` file contains:

```
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=http://localhost:9000
BUCKET_NAME=delta-bucket
```

**Note:** All environment variables are required (no default values). The `MinioDelta` class reads the bucket name from the environment, so you don't need to specify it in each method call. You can modify these values as needed. Remember to recreate the containers if you change MinIO credentials.

## Delta Lake Directory Structure

When you create a partitioned Delta table, MinIO stores:

```
delta-bucket/
└── sales_data/
    ├── _delta_log/
    │   ├── 00000000000000000000.json
    │   └── 00000000000000000001.json
    ├── category=Accessories/
    │   └── part-00000-xxxxx.parquet
    └── category=Electronics/
        └── part-00001-xxxxx.parquet
```

- **`_delta_log/`**: Transaction log (JSON files tracking each operation)
- **`category=*/`**: Partition directories (one per unique category value)
- **`.parquet` files**: Actual data in Apache Parquet format

## Useful Commands

### Docker Commands

```bash
# Start container
docker compose up -d

# Stop container
docker compose down

# Stop and remove volumes (delete all data)
docker compose down -v

# View logs
docker compose logs -f minio
```

### MinIO Console

```bash
# Access MinIO Console
open http://localhost:9001
```

## Advanced Features

### Time Travel

```python
# Read specific version
dt = DeltaTable(
    "s3://delta-bucket/sales_data",
    version=0,
    storage_options=client.storage_options
)
df_v0 = dt.to_pandas()
```

### Schema Enforcement

Delta Lake automatically enforces schema consistency:
- New data must match existing schema
- Schema evolution supported with merge operations

### Optimized Storage

- Data stored in columnar Parquet format
- Efficient compression
- Predicate pushdown for faster queries

## Troubleshooting

### Port Already in Use

If ports 9000 or 9001 are already in use, change the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "9002:9000"  # Change host port
  - "9003:9001"
```

Update `MINIO_ENDPOINT` in `.env` accordingly.

### Connection Refused

Make sure the MinIO container is running:

```bash
docker ps
docker compose logs minio
```

### Permission Errors

If you get S3 permission errors, verify:
- Bucket exists (created automatically on first write)
- Credentials are correct in `.env`
- `AWS_S3_ALLOW_UNSAFE_RENAME` is set to `"true"`

### Module Not Found

If you get import errors, install dependencies:

```bash
pip3 install uv && uv sync
```

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the image (optional)
docker rmi minio/minio
```

## Comparison: Delta Lake vs. Regular Files

| Feature | Regular Files | Delta Lake |
|---------|--------------|------------|
| ACID Transactions | ❌ | ✅ |
| Time Travel | ❌ | ✅ |
| Schema Validation | ❌ | ✅ |
| Concurrent Writes | ⚠️ Risky | ✅ Safe |
| Audit History | ❌ | ✅ |
| Data Corruption Protection | ❌ | ✅ |

## Next Steps

- Implement time travel to access historical data
- Add schema evolution examples
- Integrate with Apache Spark for large-scale processing
- Implement data quality checks with Delta Lake constraints
- Set up automated compaction and optimization (OPTIMIZE, VACUUM)
- Experiment with multi-level partitioning (e.g., by year and month)
- Add column selection to read only specific fields

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
