import os

import pytest
from dotenv import load_dotenv

from src.providers.blob_storage import BlobStorage

load_dotenv()
load_dotenv(".env.test", override=True)

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
BLOB_NAME = "sample.txt"
BLOB_DATA = "Hello from tests!"


@pytest.fixture
def blob_storage():
    client = BlobStorage()
    client.create_container(CONTAINER_NAME)
    yield client
    client.delete_container(CONTAINER_NAME)


def test_blob_storage(blob_storage):
    blob_storage.upload_blob(CONTAINER_NAME, BLOB_NAME, BLOB_DATA)

    blobs = blob_storage.list_blobs(CONTAINER_NAME)
    assert isinstance(blobs, list)
    assert BLOB_NAME in blobs

    assert blob_storage.download_blob(CONTAINER_NAME, BLOB_NAME) == BLOB_DATA
