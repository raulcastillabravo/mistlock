import os
import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "demo-project")
EMULATOR_HOST = os.getenv("FUNCTIONS_EMULATOR_HOST", "localhost:5001")
REGION = os.getenv("REGION", "us-central1")
FUNCTION_URL = f"http://{EMULATOR_HOST}/{PROJECT_ID}/{REGION}/upload_file"

def main():
    print("Testing Firebase Cloud Function...")
    print(f"Function URL: {FUNCTION_URL}\n")
    
    payload = {
        "filename": "test.txt",
        "content": "Hello from Firebase Functions!"
    }
    
    print(f"Uploading '{payload['filename']}'...")
    response = requests.post(FUNCTION_URL, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("\nCheck the Firebase Emulator UI at http://localhost:4000")

if __name__ == "__main__":
    main()
