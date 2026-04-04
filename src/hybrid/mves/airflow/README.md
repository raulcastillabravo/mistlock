# Airflow + Docker ETL Pipeline Example

Minimal viable example for Apache Airflow with Docker, demonstrating a simple ETL (Extract, Transform, Load) pipeline using Python and pandas with file-based storage.

## Project Structure

```
airflow-etl-pipeline/
├── docker-compose.yml
├── .env
├── dags/
│   ├── dag.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── logs/
├── plugins/
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Prerequisites

- Docker and Docker Compose installed
- Web browser to access Airflow UI

## Setup

### Step 1: Install Dependencies with uv

```bash
pip install uv && uv sync
```

### Step 2: Create Required Directories and Copy Files

```bash
mkdir -p dags logs plugins
```

### Step 3: Start Airflow

Start all Airflow services:

```bash
docker compose up -d
```

Wait for all services to be healthy (this may take 1-2 minutes):

```bash
docker compose ps
```

You should see all services running:

- `airflow_postgres`
- `airflow_webserver`
- `airflow_scheduler`

### Step 4: Access Airflow UI

Open your web browser and navigate to:

```
http://localhost:8080
```

Login with the default credentials:

- **Username:** `airflow`
- **Password:** `airflow`

### Step 5: Enable the DAG

1. In the Airflow UI, you should see the `etl_pipeline` DAG
2. Click the toggle switch to enable the DAG (it will turn green/blue)
3. The DAG is scheduled to run every 30 seconds automatically

### Step 6: Monitor Execution

1. Click on the DAG name to view its details
2. You'll see the Graph view showing the three tasks:
   - `extract_task` → `transform_task` → `load_task`
3. Watch as tasks execute automatically every 30 seconds
4. Each task will turn from white → light green → dark green (completed)

### Step 7: View Logs

To see detailed logs of each task:

1. Click on a task box (e.g., `extract_task`)
2. Click the task instance (date/time)
3. Click "Log" button
4. You'll see the output from each ETL step

Expected output in logs:

**Extract task:**

```
Starting data extraction...
✓ Extracted 5 rows
✓ Saved to: storage/extract/data_20240115_143052.csv

Extracted data:
   id  value category
0   1     42        A
1   2     73        B
2   3     15        C
3   4     88        A
4   5     51        B
```

**Transform task:**

```
Starting data transformation...
Reading from: storage/extract/data_20240115_143052.csv

Data before transformation:
   id  value category
0   1     42        A
1   2     73        B
2   3     15        C
3   4     88        A
4   5     51        B

✓ Transformed 5 rows
✓ Saved to: storage/transform/data_20240115_143052.csv

Data after transformation:
   id  value category
0   1     84        A
1   2    146        B
2   3     30        C
3   4    176        A
4   5    102        B
```

**Load task:**

```
Starting data loading...
Reading from: storage/transform/data_20240115_143052.csv

Data to be loaded:
   id  value category
0   1     84        A
1   2    146        B
2   3     30        C
3   4    176        A
4   5    102        B

✓ Inserted 5 rows into database
✓ Saved to: storage/load/data_20240115_143052.csv
```

### Step 8: Verify Generated Files

The generated files are stored inside the Airflow worker container. To view them:

1. Identify the Airflow worker container:

```bash
docker ps
```

2. List the files in the storage directory inside the container:

```bash
docker exec -it <worker_container_id> ls -la storage/extract/
docker exec -it <worker_container_id> ls -la storage/transform/
docker exec -it <worker_container_id> ls -la storage/load/
```

Each execution creates files with timestamps like `data_20240115_143052.csv`.

## ETL Pipeline Explanation

### Extract (extract.py)

- **Class:** `Extract`
- **Method:** `run()`
- Creates a pandas DataFrame with 5 rows and 3 columns
- Columns: `id`, `value`, `category`
- Values are randomly generated
- Saves data to `storage/extract/data_[timestamp].csv`
- Returns the file path

### Transform (transform.py)

- **Class:** `Transform`
- **Method:** `run(input_path)`
- Reads CSV from the extract directory
- Doubles the values in the `value` column
- Saves transformed data to `storage/transform/data_[timestamp].csv`
- Returns the output file path

### Load (load.py)

- **Class:** `Load`
- **Method:** `run(input_path)`
- Reads CSV from the transform directory
- Simulates a database insert
- Saves data to `storage/load/data_[timestamp].csv`
- Returns the number of rows loaded

### DAG (dag.py)

- Uses the `@dag` decorator to define the workflow
- Uses the `@task` decorator for each ETL step
- Runs every 30 seconds (`schedule_interval=timedelta(seconds=30)`)
- Tasks are chained: `extract_task >> transform_task >> load_task`
- Each task passes the file path to the next task

## Airflow Concepts

### DAG (Directed Acyclic Graph)

A collection of tasks with dependencies, representing a workflow.

### Task Decorator (@task)

Modern way to define tasks in Airflow using Python functions.

### Task Dependencies

The `>>` operator defines task execution order: `task1 >> task2` means task2 runs after task1.

### Context Manager (with)

The `@dag` decorator creates a DAG using Python's context manager pattern.

### Scheduler

Monitors DAGs and triggers task execution based on schedule (every 30 seconds in this example).

### Webserver

Provides the web UI for monitoring and managing DAGs.

## Environment Variables

The `.env` file contains:

```
AIRFLOW_USER=airflow
AIRFLOW_PASSWORD=airflow
```

## Useful Commands

### Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs of all services
docker compose logs -f

# View logs of specific service
docker compose logs -f airflow-webserver

# Restart services
docker compose restart

# Stop and remove all data
docker compose down -v
```

### Airflow CLI Commands

```bash
# List all DAGs
docker exec airflow_webserver airflow dags list

# Trigger a DAG manually
docker exec airflow_webserver airflow dags trigger etl_pipeline

# Pause a DAG
docker exec airflow_webserver airflow dags pause etl_pipeline

# Unpause a DAG
docker exec airflow_webserver airflow dags unpause etl_pipeline

# List all tasks in a DAG
docker exec airflow_webserver airflow tasks list etl_pipeline
```

### File Management Commands

```bash
# View generated files inside the worker
docker exec -it <worker_container_id> ls -la storage/extract/
docker exec -it <worker_container_id> ls -la storage/transform/
docker exec -it <worker_container_id> ls -la storage/load/

# View content of a specific file
docker exec -it <worker_container_id> cat storage/extract/data_20240115_143052.csv

# Clean up old files (optional)
docker exec -it <worker_container_id> rm storage/extract/*.csv
docker exec -it <worker_container_id> rm storage/transform/*.csv
docker exec -it <worker_container_id> rm storage/load/*.csv
```

## Troubleshooting

### Port 8080 Already in Use

Change the webserver port in `docker-compose.yml`:

```yaml
ports:
  - "8081:8080"
```

### Services Not Starting

Check logs for errors:

```bash
docker compose logs
```

Wait for the database to initialize (may take 30-60 seconds).

### DAG Not Appearing

1. Ensure DAG files are in the `dags/` directory
2. Check for Python syntax errors in DAG files
3. Wait a few seconds for Airflow to scan for new DAGs
4. Refresh the web UI



### Tasks Failing

1. Check task logs in the Airflow UI
2. Ensure pandas and numpy are installed in the Airflow container
3. Verify file paths are correct

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove generated files and directories
rm -rf logs/*
```

## Next Steps

- Add data validation and quality checks
- Implement error handling and retries
- Connect to real databases (PostgreSQL, MySQL)
- Add email notifications on failure
- Implement incremental data processing
- Add data partitioning by date
- Create data lineage tracking
- Implement data archiving strategies

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
