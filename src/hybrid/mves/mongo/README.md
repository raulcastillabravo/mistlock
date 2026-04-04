# MongoDB + MongoEngine + Docker Example

Minimal viable example to work with MongoDB using Docker Compose, MongoEngine ODM, and MongoDB Compass.

## Project Structure

```
mongo-docker-mongoengine/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── models.py
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
└── README.es.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- MongoDB Compass or any MongoDB client

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Start MongoDB Container

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify it's running:

```bash
docker ps
```

### Step 3: Create Documents and Insert Data

Run the Python script:

```bash
python main.py
```

You should see output like:

```
Connecting to MongoDB...
✓ Connected successfully

Inserting sample data...
✓ Inserted 3 users successfully

Inserted users:
  - <User(id=..., name='John Doe', email='john@example.com')>
  - <User(id=..., name='Jane Smith', email='jane@example.com')>
  - <User(id=..., name='Bob Johnson', email='bob@example.com')>

✓ Done! You can now connect with MongoDB Compass to see the data.
```

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Dependencies with uv

```bash
pip install uv && uv sync
```

### Step 2: Start MongoDB Container

```bash
docker compose up -d
```

### Step 3: Create Documents and Insert Data

```bash
python main.py
```

## Connecting with MongoDB Compass

### Step 1: Open MongoDB Compass

1. Download and install [MongoDB Compass](https://www.mongodb.com/products/compass) if you haven't already
2. Open MongoDB Compass

### Step 2: Create New Connection

Use the following connection string:

```
mongodb://admin:admin123@localhost:27017/testdb?authSource=admin
```

Or configure manually:

- **Host:** `localhost`
- **Port:** `27017`
- **Authentication:** Username/Password
  - **Username:** `admin`
  - **Password:** `admin123`
  - **Authentication Database:** `admin`
- **Database:** `testdb`

### Step 3: Connect and View Data

1. Click **Connect**
2. Navigate to the `testdb` database
3. Open the `users` collection
4. You should see the 3 users inserted by the Python script

## Database Schema

The `users` collection has the following structure:

| Field      | Type     | Description                 |
| ---------- | -------- | --------------------------- |
| \_id       | ObjectId | Auto-generated document ID  |
| name       | String   | User's full name            |
| email      | String   | User's email (unique)       |
| created_at | DateTime | Document creation timestamp |

## Environment Variables

The `.env` file contains:

```
MONGO_USER=admin
MONGO_PASSWORD=admin123
MONGO_DB=testdb
MONGO_PORT=27017
MONGO_HOST=localhost
```

You can modify these values as needed. Remember to recreate the containers if you change database credentials.

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

# View only MongoDB logs
docker compose logs -f mongodb
```

## Troubleshooting

### Port Already in Use

If port 27017 is already in use, change `MONGO_PORT` in `.env` to another port (e.g., 27018) and restart:

```bash
docker compose down
docker compose up -d
```

### Connection Refused

Make sure the MongoDB container is running:

```bash
docker ps
```

Check the logs for errors:

```bash
docker compose logs mongodb
```

### Module Not Found

If you get import errors, install dependencies:

```bash
pip3 install uv && uv sync
```

### Authentication Failed

Ensure you're using the correct credentials from the `.env` file and including `authSource=admin` in the connection string.

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the MongoDB image (optional)
docker rmi mongo:7-jammy
```

## Next Steps

- Add more document models to `models.py`
- Implement embedded documents and references
- Add data validation with MongoEngine fields
- Create indexes for better query performance
- Implement aggregation pipelines
- Add text search capabilities

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
