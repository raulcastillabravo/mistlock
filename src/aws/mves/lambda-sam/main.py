import os
import requests
from dotenv import load_dotenv


load_dotenv()

SAM_API_URL = os.getenv("SAM_API_URL")

def main():
    print("Testing Get Secret (Success)...")
    response = requests.get(f"{SAM_API_URL}/get_secret?username=admin")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}\n")

    print("Testing Get Secret (Forbidden)...")
    response = requests.get(f"{SAM_API_URL}/get_secret?username=guest")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    main()
