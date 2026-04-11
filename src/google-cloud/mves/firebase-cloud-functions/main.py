import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE") == "True"
FUNCTION_URL = os.getenv("DEBUG_FUNCTION_URL") if DEBUG_MODE else os.getenv("FUNCTION_URL")
ADMIN_USER = os.getenv("ADMIN_USER")

def request_secret(username: str) -> str | None:
    response = requests.get(FUNCTION_URL, params={"username": username})

    return response.json().get('secret') if response.status_code == 200 else None

def main() -> None:
    print(f"Calling function: {FUNCTION_URL}")
    print(f'Scenario 1 (admin user). Secret: {request_secret(ADMIN_USER)}')
    print(f'Scenario 2 (guest user). Secret: {request_secret('guest')}')

if __name__ == "__main__":
    main()
