from src.providers.redis_client import RedisClient

def test_redis_client_success():
    with RedisClient() as client:
        client.set("test_key", "test_value")
        value = client.get("test_key")
        assert value == "test_value"
        client.delete("test_key")

def test_redis_client_methods():
    rc = RedisClient()
    client = rc.connect()
    assert client.ping() is True
    rc.close()

def test_redis_client_context_manager():
    rc = RedisClient()
    with rc as client:
        assert client.ping() is True
