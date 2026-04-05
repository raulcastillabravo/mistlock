import os
from azure.storage.blob import BlobServiceClient

class AzuriteClient:
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
    
    def create_container(self, container_name):
        """Create a container if it doesn't exist."""
        container_client = self.blob_service_client.get_container_client(
            container_name
        )
        if not container_client.exists():
            container_client.create_container()
    
    def upload_blob(self, container_name, blob_name, data):
        """Upload data to a blob."""
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )
        blob_client.upload_blob(data, overwrite=True)
