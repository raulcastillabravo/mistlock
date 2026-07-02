from src.providers.blob_storage import BlobStorage

CONTAINER_NAME = "test-blob-storage"
BLOB_NAME = "sample.txt"
BLOB_DATA = "Hello from tests!"


def test_blob_storage():
    client = BlobStorage()

    client.create_container(CONTAINER_NAME)
    client.upload_blob(CONTAINER_NAME, BLOB_NAME, BLOB_DATA)

    blobs = client.list_blobs(CONTAINER_NAME)
    assert isinstance(blobs, list)
    assert BLOB_NAME in blobs

    assert client.download_blob(CONTAINER_NAME, BLOB_NAME) == BLOB_DATA
