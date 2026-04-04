# Redis + Python + Docker Example

Minimal viable example to work with Redis using Docker Compose, Python redis client, and Redis Insight.

## Project Structure

```
redis-docker-python/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── redis_client.py
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- Redis Insight or any Redis client

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Start Redis Container

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify it's running:

```bash
docker ps
```

### Step 3: Run Redis Operations

Execute the Python script:

```bash
python main.py
```

You should see output like:

```

--- Setting user data with HSET ---

--- Retrieving specific fields with HGET ---

User 1001 details:
  Name: John Doe
  Email: john@example.com

✓ Done! You can now see the data in Redis Insight.
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Dependencies with uv

```bash
pip install uv && uv sync
```

### Step 2: Start Redis Container

```bash
docker compose up -d
```

### Step 3: Run Redis Operations

```bash
python main.py
```

## Connecting with Redis Insight

### Step 1: Install Redis Insight

1. Download and install [Redis Insight](https://redis.io/insight/) if you haven't already
2. Open Redis Insight

### Step 2: Add Database Connection

1. Click on **Add Redis Database**
2. Select **Add Database Manually**
3. Configure the connection:
   - **Host:** `localhost`
   - **Port:** `6379`
   - **Database Alias:** `Local Redis` (or any name you prefer)
   - **Username:** leave empty
   - **Password:** `redis123`
4. Click **Add Redis Database**

### Step 3: View Data

1. Click on your database connection
2. Go to the **Browser** tab
3. You should see the hash keys: `user:1001`, `user:1002`, `user:1003`
4. Click on any key to view its fields and values

## Redis Data Structure

This example uses Redis **Hash** data type to store user information:

| Key        | Field | Value              |
| ---------- | ----- | ------------------ |
| user:1001  | name  | John Doe           |
| user:1001  | email | john@example.com   |
| user:1001  | age   | 30                 |

## Environment Variables

The `.env` file contains:

```
REDIS_PASSWORD=redis123
REDIS_PORT=6379
REDIS_HOST=localhost
```

You can modify these values as needed. Remember to recreate the containers if you change Redis password.

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

# View only Redis logs
docker compose logs -f redis
```

### Redis CLI Commands

```bash
# Connect to Redis CLI from container
docker exec -it redis_local redis-cli -a redis123

# Get all keys
KEYS *

# Get all fields from a hash
HGETALL user:1001

# Get specific field
HGET user:1001 name

# Delete a key
DEL user:1001

# Exit Redis CLI
exit
```

## Redis Operations Explained

### HSET (Hash Set)
Sets a field in a hash to a value. If the hash doesn't exist, it's created.

```python
redis.client.hset("user:1001", "name", "John Doe")
```

Redis equivalent:
```
HSET user:1001 name "John Doe"
```

### HGET (Hash Get)
Gets the value of a specific field in a hash.

```python
name = redis.client.hget("user:1001", "name")
```

Redis equivalent:
```
HGET user:1001 name
```

### HGETALL (Hash Get All)
Gets all fields and values in a hash.

```python
user_data = redis.client.hgetall("user:1001")
```

Redis equivalent:
```
HGETALL user:1001
```

## Troubleshooting

### Port Already in Use

If port 6379 is already in use, change `REDIS_PORT` in `.env` to another port (e.g., 6380) and restart:

```bash
docker compose down
docker compose up -d
```

### Connection Refused

Make sure the Redis container is running:

```bash
docker ps
```

Check the logs for errors:

```bash
docker compose logs redis
```

### Module Not Found

If you get import errors, install dependencies:

```bash
pip3 install uv && uv sync
```

### Authentication Failed

Ensure you're using the correct password from the `.env` file when connecting.

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the Redis image (optional)
docker rmi redis:7-alpine
```

## Next Steps

- Explore other Redis data types (Lists, Sets, Sorted Sets, Streams)
- Implement caching patterns
- Add expiration times with TTL
- Use Redis pub/sub for messaging
- Implement distributed locking
- Add Redis transactions

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.