import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

class AzuriteClient:
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    def create_container(self, container_name):
        """Create a container if it doesn't exist."""
        container_client = self.blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            print(f"Container '{container_name}' created.")
        else:
            print(f"Container '{container_name}' already exists.")
    
    def upload_blob(self, container_name, blob_name, data):
        """Upload data to a blob."""
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )
        blob_client.upload_blob(data, overwrite=True)
        print(f"Uploaded '{blob_name}' to container '{container_name}'.")
    
    def download_blob(self, container_name, blob_name):
        """Download blob content."""
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )
        return blob_client.download_blob().readall().decode('utf-8')
    
    def list_blobs(self, container_name):
        """List all blobs in a container."""
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]
