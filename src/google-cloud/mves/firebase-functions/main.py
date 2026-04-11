import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE") == "True"
FUNCTION_URL = os.getenv("DEBUG_FUNCTION_URL") if DEBUG_MODE else os.getenv("FUNCTION_URL")
ADMIN_USER = os.getenv("ADMIN_USER")

def main() -> None:
    """
    Main execution logic to call the Cloud Function.
    """
    print(f"Calling function: {FUNCTION_URL}")
    
    # 1. Success scenario
    print(f"Scenario 1: Authorized access for user {ADMIN_USER}")
    params = {"username": ADMIN_USER}
    
    try:
        response = requests.get(FUNCTION_URL, params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Secret: {data.get('secret')}")
        else:
            print(f"Response Body: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the service. Is it running?")
        return

    # 2. Failure scenario
    print("\nScenario 2: Access denied (wrong_user)")
    params = {"username": "wrong_user"}
    response = requests.get(FUNCTION_URL, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    main()
