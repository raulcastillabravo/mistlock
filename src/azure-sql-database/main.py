import requests
import json
import time

# Azure Function endpoint
FUNCTION_URL = "http://localhost:7071/api/users"

def register_test_user(name, email):
    """Send a POST request to register a user.
    
    Args:
        name: User's name
        email: User's email
    """
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
    print("Welcome to Azure SQL + Azure Functions MVE")
    print("-" * 40)
    
    # Example data
    test_users = [
        {"name": "Raul Castilla", "email": "raul@example.com"},
        {"name": "John Doe", "email": "john.doe@example.com"}
    ]
    
    for user in test_users:
        register_test_user(user["name"], user["email"])
        time.sleep(1)
    
    print("-" * 40)
    print("Verification:")
    print("1. Use VS Code SQL Server extension to query 'Users' table in 'UserDB'")
    print("2. Or use DBeaver connected to localhost:1433")
