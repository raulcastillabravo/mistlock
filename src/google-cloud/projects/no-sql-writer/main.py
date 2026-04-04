import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8080")
url = f"{SERVICE_URL}:{SERVICE_PORT}"

def main():
    print(f"Connecting to Cloud Run Service at {url}...")

    patient_data = {
        "name": "Jane",
        "surname": "Doe",
        "dni": "12345678X",
    }

    print(f"Admitting: {patient_data['name']} {patient_data['surname']}...")
    response = requests.post(
        url,
        json=patient_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 201:
        print("Success! Patient admitted.")
        print("Response:", response.json())
    else:
        print(f"Failed. Status: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    main()
