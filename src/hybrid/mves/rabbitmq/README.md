# RabbitMQ + Python + Docker Example

Minimal viable example to work with RabbitMQ using Docker Compose, Python pika client, and RabbitMQ Management UI.

## Project Structure

```
rabbitmq-docker-python/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── rabbitmq_client.py
├── publish.py
├── listen.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- Web browser to access RabbitMQ Management UI

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Start RabbitMQ Container

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify it's running:

```bash
docker ps
```

### Step 3: Publish Events

Open a terminal and run the publisher:

```bash
python publish.py
```

You should see output like:

```
--- Publishing event to RabbitMQ ---
✓ Published: User logged in: jane@example.com

✓ Done! Event published to queue 'user_events'
✓ You can run listen.py to consume this event
```

Each time you run `publish.py`, it will publish one random event from the available options.

### Step 4: Listen to Events

Open a **new terminal** (keep the first one open) and run the listener:

```bash
python listen.py
```

You should see:

```
--- Listening for events on queue 'user_events' ---
✓ Waiting for messages. Press CTRL+C to exit

✓ Received: User logged in: jane@example.com
```

The listener will keep running and waiting for new events. Press `CTRL+C` to stop it.

### Step 5: Test Real-time Event Processing

With `listen.py` still running, open another terminal and publish more events:

```bash
python publish.py
```

You'll see the listener immediately receive and process the new event. Each execution of `publish.py` sends one random event to the queue.

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Dependencies with uv

```bash
pip install uv && uv sync
```

### Step 2: Start RabbitMQ Container

```bash
docker compose up -d
```

### Step 3: Publish and Listen to Events

Follow steps 3-5 from Option 1.

## Accessing RabbitMQ Management UI

RabbitMQ comes with a web-based management interface that allows you to monitor queues, exchanges, connections, and more.

### Step 1: Open the Management UI

Open your web browser and navigate to:

```
http://localhost:15672
```

### Step 2: Login

Use the credentials from your `.env` file:

- **Username:** `admin`
- **Password:** `admin123`

### Step 3: View Queues

1. Click on the **Queues** tab at the top
2. You should see the `user_events` queue
3. Click on the queue name to see detailed statistics:
   - Number of messages ready
   - Number of messages being delivered
   - Message rates
   - Consumer details

### Step 4: View Messages

While viewing a queue, scroll down to the **Get messages** section to inspect messages without removing them from the queue.

## RabbitMQ Concepts

### Queue
A buffer that stores messages. Producers send messages to queues, and consumers receive messages from queues.

### Producer (Publisher)
An application that sends messages to a queue. In this example, `publish.py` is the producer.

### Consumer (Listener)
An application that receives messages from a queue. In this example, `listen.py` is the consumer.

### Message Acknowledgment
When a consumer processes a message, it sends an acknowledgment (ack) to RabbitMQ. This ensures that messages aren't lost if a consumer fails.

### Durable Queue
A queue that survives RabbitMQ restarts. Messages in durable queues are persisted to disk.

## Environment Variables

The `.env` file contains:

```
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin123
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_MANAGEMENT_PORT=15672
```

- **Port 5672**: AMQP protocol (for applications)
- **Port 15672**: Management UI (for web browser)

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

# View only RabbitMQ logs
docker compose logs -f rabbitmq
```

### RabbitMQ CLI Commands

```bash
# List all queues
docker exec rabbitmq_local rabbitmqctl list_queues

# List all exchanges
docker exec rabbitmq_local rabbitmqctl list_exchanges

# Purge a queue (delete all messages)
docker exec rabbitmq_local rabbitmqctl purge_queue user_events
```

## Troubleshooting

### Port Already in Use

If ports 5672 or 15672 are already in use, change the ports in `.env`:

```
RABBITMQ_PORT=5673
RABBITMQ_MANAGEMENT_PORT=15673
```

Then restart:

```bash
docker compose down
docker compose up -d
```

### Connection Refused

Make sure the RabbitMQ container is running:

```bash
docker ps
```

Check the logs for errors:

```bash
docker compose logs rabbitmq
```

Wait a few seconds after starting the container for RabbitMQ to fully initialize.

### Module Not Found

If you get import errors, install dependencies:

```bash
pip3 install uv && uv sync
```

### Authentication Failed

Ensure you're using the correct credentials from the `.env` file.

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the RabbitMQ image (optional)
docker rmi rabbitmq:3-management-alpine
```

## Next Steps

- Implement multiple consumers for load balancing
- Use exchanges and routing keys for message routing
- Implement dead letter queues for failed messages
- Add message priorities
- Explore RabbitMQ clustering for high availability
- Implement RPC (Remote Procedure Call) patterns

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.