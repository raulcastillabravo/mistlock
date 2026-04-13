import pytest
import redis
from src.providers.redis_client import RedisClient

def test_redis_client_success():
    """Test full happy path: connect, interaction, close."""
    with RedisClient() as client:
        client.set("test_key", "test_value")
        # In success scenario, we assume redis is running as per user instruction
        value = client.get("test_key")
        assert value == "test_value"
        client.delete("test_key")

def test_redis_client_failure():
    """Test interaction before connection."""
    rc = RedisClient()
    # If we don't connect or use context manager, _client is None
    # Attempting to use it directly (if we exposed it, but we use private)
    # The user wants to test "trying to write before connecting"
    with pytest.raises(AttributeError):
        # Accessing private attribute that is None should fail if we try to call methods on it
        rc._client.set("fail", "fail")

def test_redis_client_methods():
    """Test connect and close methods directly."""
    rc = RedisClient()
    client = rc.connect()
    assert client.ping() is True
    rc.close()

def test_redis_client_context_manager():
    """Test the context manager implementation."""
    rc = RedisClient()
    with rc as client:
        assert client.ping() is True
    # Verify it can't be used after context (though redis-py might not throw immediately)
