import os
import uuid
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "TestDB"
CONTAINER_NAME = "TestContainer"

def run():
    print(f"--- Cosmos DB Connection Test ---")
    print(f"Endpoint: {COSMOS_ENDPOINT}")
    
    client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    
    print(f"Connecting to database: {DATABASE_NAME}...")
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    
    print(f"Connecting to container: {CONTAINER_NAME}...")
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME, 
        partition_key=PartitionKey(path="/category"),
        offer_throughput=400
    )
    
    test_id = str(uuid.uuid4())
    test_item = {
        "id": test_id,
        "message": "Hello from local Python script!",
        "category": "testing",
    }
    
    print(f"Uploading test item with ID: {test_id}...")
    container.upsert_item(test_item)
    
    print(f"SUCCESS: Item uploaded successfully to Cosmos DB!")
    print("Check it out at http://localhost:1234/")
        

if __name__ == "__main__":
    run()
