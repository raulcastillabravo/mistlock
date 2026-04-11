import os
import requests
from dotenv import load_dotenv

def main() -> None:
    """
    Client script to call the get_secret Cloud Function.
    """
    load_dotenv()
    
    # Configuration
    project_id = os.getenv("FIREBASE_PROJECT", "demo-mve-firebase-functions")
    admin_user = os.getenv("ADMIN_USER", "admin")
    region = "us-central1"
    function_name = "get_secret"
    
    # Emulator URL
    # Firebase Emulator default port for functions is 5001
    url = f"http://localhost:5001/{project_id}/{region}/{function_name}"
    
    print(f"Calling function: {url}")
    
    # 1. Success scenario
    print(f"\nScenario 1: Authorized access ({admin_user})")
    params = {"username": admin_user}
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Secret: {data.get('secret')}")
        else:
            print(f"Response Body: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Firebase Emulator. Is it running?")
        return

    # 2. Failure scenario
    print("\nScenario 2: Access denied (wrong_user)")
    params = {"username": "wrong_user"}
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    main()
