import os
from dotenv import load_dotenv
from azurite_client import AzuriteClient

load_dotenv()

CONTAINER_NAME = os.getenv("CONTAINER_NAME", "test-container")

def main():
    print("Connecting to Azurite...")
    
    client = AzuriteClient()
    
    # Create container
    client.create_container(CONTAINER_NAME)
    
    # Upload a blob
    print("\nUploading blob...")
    client.upload_blob(
        container_name=CONTAINER_NAME,
        blob_name="hello.txt",
        data="Hello from Azurite!"
    )
    
    # List blobs
    print("\nListing blobs in container:")
    blobs = client.list_blobs(CONTAINER_NAME)
    for blob in blobs:
        print(f"  - {blob}")
    
    # Download blob
    print("\nDownloading blob...")
    content = client.download_blob(CONTAINER_NAME, "hello.txt")
    print(f"Content: {content}")

if __name__ == "__main__":
    main()
