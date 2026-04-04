# Redis Distributed Mutex + Python + Docker Example

Minimal viable example to implement a distributed mutex (lock) using Redis with Docker Compose and Python. This example demonstrates how to safely coordinate access to shared resources across multiple threads or processes.

## Project Structure

```
redis-docker-mutex/
├── .devcontainer/
│   └── devcontainer.json
├── .vscode/
│   └── settings.json
├── docker-compose.yml
├── .env
├── redis_client.py
├── mutex.py
├── main.py
├── main_acquire.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- Python 3.12+ (if running locally without dev container)

## What is a Distributed Mutex?

A **mutex** (mutual exclusion) is a synchronization mechanism that prevents multiple threads or processes from accessing a shared resource simultaneously. A **distributed mutex** extends this concept across multiple machines or processes, using an external service (like Redis) as a coordination point.

### Use Cases:

- **Prevent race conditions**: When multiple processes write to the same file or database
- **Ensure data consistency**: When updating shared data structures
- **Job scheduling**: Prevent duplicate execution of scheduled tasks
- **Resource allocation**: Coordinate access to limited resources

## How This Example Works

The example creates 5 threads that all try to write to the same file (`shared_file.txt`). The threads start simultaneously and compete for the mutex lock. The Redis mutex ensures that only one thread can write at a time, demonstrating true concurrent behavior where acquisition order is non-deterministic.

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

### Step 3: Run the Mutex Examples

Execute the Python scripts:

**Example 1: Using explicit lock/unlock**
```bash
python main.py
```

**Example 2: Using acquire context manager**
```bash
python main_acquire.py
```

You should see output like:

```
[Thread 1] ✓ Done
[Thread 3] ✓ Done
[Thread 2] ✓ Done
[Thread 5] ✓ Done
[Thread 4] ✓ Done
```

The file `shared_file.txt` will contain:

```
Thread 1 wrote this line
Thread 3 wrote this line
Thread 2 wrote this line
Thread 5 wrote this line
Thread 4 wrote this line
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

### Step 3: Run the Mutex Examples

```bash
python main.py
# or
python main_acquire.py
```

## Understanding the Mutex Implementation

### Key Features

The `RedisMutex` class inherits from `RedisClient` and provides:

#### 1. `lock(resource, wait_sec, retry_sec)` - Acquire a lock

```python
if mutex.lock("my_resource", wait_sec=10.0, retry_sec=0.5):
    # Lock acquired, do work
    mutex.unlock("my_resource")
else:
    # Could not acquire lock within timeout
    print("Timeout acquiring lock")
```

- **resource**: Name of the resource to lock (string)
- **wait_sec**: Maximum time to wait for the lock (default: 10.0 seconds)
- **retry_sec**: Time between retry attempts (default: 0.1 seconds)
- **Returns**: `True` if lock acquired, `False` if timeout

#### 2. `unlock(resource)` - Release the lock

```python
mutex.unlock("my_resource")
```

Releases the specified lock. Must provide the resource name to unlock.

#### 3. `acquire(resource, wait_sec, retry_sec)` - Context Manager (Recommended)

```python
try:
    with mutex.acquire("my_resource", wait_sec=5.0, retry_sec=0.5):
        # Critical section - only one thread can be here at a time
        write_to_file("shared_file.txt", "data")
        # Lock is automatically released here
except LockAcquisitionError as e:
    print(f"Could not acquire lock: {e}")
```

This is the **recommended approach** for the lock/unlock pattern because it ensures the lock is always released, even if an exception occurs.

#### 4. Context Manager for Connection Management

```python
with RedisMutex() as mutex:
    # Use mutex here
    # Connection is automatically closed when exiting
```

### How It Works Internally

1. **Inheritance**: `RedisMutex` inherits from `RedisClient` and manages its own connection
2. **Lock Acquisition**: Uses Redis `SET` command with `NX` (set if Not eXists) option - atomic operation
3. **Expiration**: Locks automatically expire after 30 seconds to prevent deadlocks
4. **Retry Logic**: If lock cannot be acquired, waits `retry_sec` and tries again
5. **Timeout**: If `wait_sec` is exceeded, returns `False` (for `lock()`) or raises `LockAcquisitionError` (for `acquire()`)
6. **Resource Cleanup**: Connection is closed via `close()` method or context manager

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
docker exec -it redis_mutex redis-cli -a redis123

# View active locks
KEYS lock:*

# Check if a specific lock exists
GET lock:my_resource

# Manually delete a lock (use with caution!)
DEL lock:my_resource

# Exit Redis CLI
exit
```

## Code Examples

### Example 1: Using explicit lock/unlock (main.py)

```python
import threading
import time
import random
from mutex import RedisMutex

def write_to_file(thread_id: int):
    mutex = RedisMutex()
    resource = "file_write_lock"
    filename = "shared_file.txt"
    lock_acquired = False

    try:
        if not mutex.lock(resource, wait_sec=15.0, retry_sec=0.5):
            print(f"[Thread {thread_id}] X Unable to lock")
            return
        
        lock_acquired = True
        time.sleep(random.uniform(0.1, 0.5))  # Variable processing time
        with open(filename, 'a') as f:
            f.write(f"Thread {thread_id} wrote this line\n")
        print(f"[Thread {thread_id}] ✓ Done")
    finally:
        if lock_acquired:
            mutex.unlock(resource)
        mutex.close()

def main():
    threads = []
    
    for i in range(5):
        thread = threading.Thread(target=write_to_file, args=[i + 1])
        threads.append(thread)
        thread.start() 
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
```

### Example 2: Using acquire context manager (main_acquire.py)

```python
import threading
import time
import random
from mutex import RedisMutex, LockAcquisitionError

def write_to_file(thread_id: int):
    mutex = RedisMutex()
    resource = "file_write_lock"
    filename = "shared_file.txt"

    try:
        with mutex.acquire(resource, wait_sec=15.0, retry_sec=0.5):
            time.sleep(random.uniform(0.1, 0.5))  # Variable processing time
            with open(filename, 'a') as f:
                f.write(f"Thread {thread_id} wrote this line\n")
            print(f"[Thread {thread_id}] ✓ Done")
    except LockAcquisitionError:
        print(f"[Thread {thread_id}] X Unable to lock")
    finally:
        mutex.close()

def main():
    threads = []
    
    for i in range(5):
        thread = threading.Thread(target=write_to_file, args=[i + 1])
        threads.append(thread)
        thread.start() 
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
```

### Example 3: Using RedisMutex as context manager

```python
from mutex import RedisMutex, LockAcquisitionError

def write_to_file(thread_id: int, filename: str):
    # Connection management with context manager
    with RedisMutex() as mutex:
        try:
            with mutex.acquire("file_write_lock", wait_sec=15.0):
                with open(filename, 'a') as f:
                    f.write(f"Thread {thread_id} writing\n")
        except LockAcquisitionError as e:
            print(f"Error: {e}")
    # Connection is automatically closed
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

### Lock Times Out Immediately

- Verify Redis is running: `docker ps`
- Check Redis connection: `docker exec -it redis_mutex redis-cli -a redis123 PING`
- Ensure `.env` file exists and has correct credentials

### Lock Never Released

If a lock is stuck (e.g., process crashed), you can manually delete it:

```bash
docker exec -it redis_mutex redis-cli -a redis123 DEL lock:resource_name
```

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the Redis image (optional)
docker rmi redis:7-alpine

# Delete the shared file created by the example
rm shared_file.txt
```

## Best Practices

1. **Use context managers**: 
   - Use `with RedisMutex() as mutex:` for connection management
   - Use `with mutex.acquire():` for lock management
2. **Set appropriate timeouts**: Balance between too short (false failures) and too long (poor user experience)
3. **Handle exceptions**: Always catch and handle `LockAcquisitionError` gracefully
4. **Keep critical sections short**: Minimize the time you hold a lock
5. **Use descriptive resource names**: Make it clear what each lock protects
6. **Close connections explicitly**: Call `mutex.close()` or use context manager
7. **Monitor lock expiration**: The default 30-second expiration prevents deadlocks but may be too short for long operations

## Design Decisions

### Why `SET` with `NX` instead of `HSET`?

- **Atomic operation**: `SET` with `nx=True` only creates the key if it doesn't exist
- **Automatic expiration**: `ex=30` prevents orphaned locks if a process dies
- **Official Redis pattern**: Recommended by Redis for distributed locks
- **Simple and efficient**: Single operation, no additional complexity

### Why does `lock()` return `False` instead of raising an exception?

- **Flexibility**: Allows for different error handling strategies
- **Explicit control flow**: `if not mutex.lock()` is clear and readable
- **context manager still raises**: `acquire()` raises `LockAcquisitionError` for cleaner exception handling

### Why does `RedisMutex` inherit from `RedisClient`?

- **Encapsulation**: Each mutex manages its own connection lifecycle
- **Simplicity**: No need to pass around `RedisClient` instances
- **Thread-safe**: Each thread can create its own mutex with isolated connection

## Limitations and Considerations

- **Single Redis instance**: This example uses a single Redis instance. For production, consider Redis Cluster or Redis Sentinel for high availability
- **Lock expiration**: Locks expire after 30 seconds to prevent deadlocks. Adjust this based on your needs
- **Not suitable for very high throughput**: If you need thousands of lock operations per second, consider other solutions
- **Network dependency**: The mutex reliability depends on network stability
- **Multiple connections**: Each `RedisMutex` instance creates its own connection (uses Redis connection pooling internally)

## Next Steps

- Implement lock renewal for long-running operations
- Add distributed semaphores (allow N concurrent accesses)
- Implement read/write locks
- Add lock ownership verification with unique identifiers
- Explore Redis RedLock algorithm for multi-node setups
- Add metrics and monitoring for lock contention
- Implement shared connection pool for high-performance scenarios

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
