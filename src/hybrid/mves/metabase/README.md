# Metabase + PostgreSQL + Docker Example

Minimal viable example to work with Metabase using Docker Compose, PostgreSQL as data source, and SQLAlchemy ORM.

## Project Structure

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── .env
├── db.py
├── models.py
├── pyproject.toml
├── main.py
├── uv.lock
└── README.md
```

## Prerequisites

- Docker and Docker Compose installed
- VS Code with Dev Containers extension (optional, for dev container setup)
- DBeaver or any PostgreSQL client (optional)

## Option 1: Using Dev Container (Recommended)

### Step 1: Open Project in Dev Container

1. Open VS Code in the project folder
2. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Type and select: **Dev Containers: Reopen in Container**
4. Wait for the container to build and dependencies to install

### Step 2: Start Services

Inside the dev container terminal:

```bash
docker compose up -d
```

Verify services are running:

```bash
docker ps
```

You should see two containers: `metabase` and `postgres_metabase`.

### Step 3: Create Tables and Insert Sample Data

Run the Python script:

```bash
python main.py
```

You should see output like:

```
Inserted 25 products into the database
```

This will create the `products` table in the `metabaseappdb` database and insert 25 sample products with pre-calculated data.

### Step 4: Access Metabase

1. Open your browser and go to: **http://localhost:3000**
2. Complete the initial setup:
   - Create your admin account
   - Click "Add your data"
   - Select **PostgreSQL**
   - Enter connection details:
     - **Host:** `postgres`
     - **Port:** `5432`
     - **Database name:** `metabaseappdb`
     - **Username:** `metabase`
     - **Password:** `metabase123`
3. Click **Save**
4. Start exploring your data and creating visualizations!

## Option 2: Local Setup (Without Dev Container)

### Step 1: Install Python Dependencies

```bash
pip3 install uv && uv sync
```

### Step 2: Start Services

```bash
docker compose up -d
```

### Step 3: Create Tables and Insert Data

```bash
python main.py
```

### Step 4: Access Metabase

Follow Step 4 from Option 1 above.

## Database Schema

The `products` table has the following structure:

| Column        | Type                  | Description                    |
|---------------|-----------------------|--------------------------------|
| id            | INTEGER (Primary Key) | Auto-incrementing product ID   |
| name          | VARCHAR(200)          | Product name                   |
| category      | VARCHAR(100)          | Product category               |
| price         | FLOAT                 | Unit price                     |
| quantity_sold | INTEGER               | Number of units sold           |
| revenue       | FLOAT                 | Total revenue (price * qty)    |
| sale_date     | TIMESTAMP             | Sale date                      |

## Sample Data

The script inserts 25 sample products across 5 categories:
- **Electronics** (5 products): Laptops, phones, TVs, headphones, smartwatches
- **Clothing** (5 products): Sneakers, jeans, jackets, t-shirts, coats
- **Home & Kitchen** (5 products): Mixers, coffee machines, vacuums, air fryers, cookware
- **Books** (5 products): Classic literature and business books
- **Sports & Outdoors** (5 products): Yoga mats, dumbbells, bikes, tents, running shoes

## Environment Variables

The `.env` file contains:

```
METABASE_USER=metabase
METABASE_PASSWORD=metabase123
METABASE_DB=metabaseappdb
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

You can modify these values as needed. Remember to recreate the containers if you change database credentials.

## Connecting with DBeaver (Optional)

### Step 1: Create New Connection

1. Open DBeaver
2. Click on **New Database Connection** (plug icon with +)
3. Select **PostgreSQL**
4. Click **Next**

### Step 2: Configure Connection

Enter the following details:

- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `metabaseappdb`
- **Username:** `metabase`
- **Password:** `metabase123`

### Step 3: Test and Save

1. Click **Test Connection** to verify
2. If successful, click **Finish**

### Step 4: View Data

1. In the Database Navigator, expand your connection
2. Navigate to: `metabaseappdb` → `Schemas` → `public` → `Tables` → `products`
3. Right-click on `products` table → **View Data**
4. You should see the 25 products inserted by the Python script

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

# View only Metabase logs
docker compose logs -f metabase

# View only PostgreSQL logs
docker compose logs -f postgres
```

### Metabase Commands

```bash
# Check if Metabase is ready
curl http://localhost:3000/api/health
```

## Creating Visualizations in Metabase

Once you've connected Metabase to PostgreSQL, you can create various visualizations:

### Example Questions to Ask:

1. **Total Revenue by Category**
   - Visualization: Bar chart or Pie chart
   - Group by: `category`
   - Summarize: Sum of `revenue`

2. **Units Sold Over Time**
   - Visualization: Line chart
   - X-axis: `sale_date`
   - Y-axis: Sum of `quantity_sold`

3. **Top 10 Products by Revenue**
   - Visualization: Bar chart
   - Sort by: `revenue` (descending)
   - Limit: 10

4. **Average Price by Category**
   - Visualization: Bar chart
   - Group by: `category`
   - Summarize: Average of `price`

## Troubleshooting

### Port Already in Use

If port 3000 or 5432 is already in use, change the port mappings in `docker-compose.yml` and restart:

```bash
docker compose down
docker compose up -d
```

### Metabase Not Loading

Wait a minute for Metabase to fully start up. Check the health status:

```bash
docker compose logs -f metabase
```

Look for the message: "Metabase Initialization COMPLETE"

### Connection Refused

Make sure both containers are running:

```bash
docker ps
```

Check the logs for errors:

```bash
docker compose logs postgres
docker compose logs metabase
```

### Module Not Found

If you get import errors, install dependencies:

```bash
pip3 install uv && uv sync
```

### Permission Denied (Dev Container)

If you get permission errors with Docker in the dev container, make sure the `docker-outside-of-docker` feature is properly configured in `devcontainer.json`.

## Clean Up

To completely remove everything:

```bash
# Stop and remove containers and volumes
docker compose down -v

# Remove the images (optional)
docker rmi metabase/metabase:latest postgres:15-alpine
```

## Next Steps

- Create more complex queries and dashboards in Metabase
- Add more product data with different date ranges
- Implement data relationships (e.g., customers, orders)
- Set up automated email reports in Metabase
- Configure user permissions and sharing in Metabase
- Add more tables to create a complete e-commerce database

## License

This is a minimal example for educational purposes. Feel free to use and modify as needed.
