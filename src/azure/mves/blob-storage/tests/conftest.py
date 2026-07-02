import os

import pytest
from dotenv import load_dotenv

from src.providers.blob_storage import BlobStorage

load_dotenv()
load_dotenv(".env.test", override=True)


@pytest.fixture
def blob_storage():
    client = BlobStorage()
    container_name = os.getenv("CONTAINER_NAME")
    client.create_container(container_name)
    yield client
    client.delete_container(container_name)
