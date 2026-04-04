import requests
from dotenv import load_dotenv

load_dotenv()

FUNCTION_URL = "http://localhost:7071/api/upload"

def main():
    print("Testing Azure Function upload endpoint...")
    filename = "test.txt"
    file_content = "Hello from Azure Functions!"
    print(f"\nUploading '{filename}'...")
    response = requests.post(
        FUNCTION_URL,
        params={"filename": filename},
        data=file_content.encode('utf-8'),
        headers={"Content-Type": "text/plain"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    main()


