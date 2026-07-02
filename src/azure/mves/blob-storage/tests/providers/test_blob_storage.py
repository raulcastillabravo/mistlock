import os

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
BLOB_NAME = "sample.txt"
BLOB_DATA = "Hello from tests!"


def test_blob_storage(blob_storage):
    blob_storage.upload_blob(CONTAINER_NAME, BLOB_NAME, BLOB_DATA)

    blobs = blob_storage.list_blobs(CONTAINER_NAME)
    assert isinstance(blobs, list)
    assert BLOB_NAME in blobs

    assert blob_storage.download_blob(CONTAINER_NAME, BLOB_NAME) == BLOB_DATA
