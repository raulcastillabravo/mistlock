import os
import requests
from dotenv import load_dotenv

load_dotenv()

FUNCTION_URL = os.getenv("FUNCTION_URL")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")


def main():
    users = [ADMIN_USERNAME, "guest", "unknown"]

    print("Testing Azure Function: get_secret\n")

    for user in users:
        print(f"Checking access for user: {user}")
        response = requests.get(FUNCTION_URL, params={"username": user})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")


if __name__ == "__main__":
    main()
