import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Azure Function endpoint
FUNCTION_URL = os.getenv("FUNCTION_URL")

def register_test_user(name, email):
    payload = {
        "name": name,
        "email": email
    }
    
    print(f"Sending POST request to {FUNCTION_URL}...")
    try:
        response = requests.post(
            FUNCTION_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print(f"✓ Success: {response.text}")
        else:
            print(f"✗ Failed (Status {response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the Azure Function. Is it running?")

if __name__ == "__main__":
    test_users = [
        {"name": "Raul Castilla", "email": "raul@example.com"},
        {"name": "John Doe", "email": "john.doe@example.com"}
    ]
    
    for user in test_users:
        register_test_user(user["name"], user["email"])
