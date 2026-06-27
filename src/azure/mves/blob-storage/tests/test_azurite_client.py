from azurite_client import AzuriteClient

CONTAINER_NAME = "test-azurite-client"
BLOB_NAME = "sample.txt"
BLOB_DATA = "Hello from tests!"


def test_blob_roundtrip():
    client = AzuriteClient()

    client.create_container(CONTAINER_NAME)
    client.upload_blob(CONTAINER_NAME, BLOB_NAME, BLOB_DATA)

    assert BLOB_NAME in client.list_blobs(CONTAINER_NAME)
    assert client.download_blob(CONTAINER_NAME, BLOB_NAME) == BLOB_DATA
