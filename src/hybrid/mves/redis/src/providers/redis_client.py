import os
from typing import Optional, Type

import redis
from dotenv import load_dotenv


class RedisClient:
    """Class to manage the Redis connection as a context manager."""

    _host: str = None
    _port: int = None
    _password: Optional[str] = None
    _client: Optional[redis.Redis] = None

    def __init__(self) -> None:
        load_dotenv()
        self._host = os.getenv("REDIS_HOST")
        self._port = int(os.getenv("REDIS_PORT"))
        self._password = os.getenv("REDIS_PASSWORD")

    def connect(self) -> redis.Redis:
        """Connect to the Redis server."""
        self._client = redis.Redis(
            host=self._host,
            port=self._port,
            password=self._password,
            decode_responses=True,
        )
        return self._client

    def close(self) -> None:
        """Close the Redis connection."""
        if self._client:
            self._client.close()

    def __enter__(self) -> redis.Redis:
        """Connect to the Redis server when entering the context."""
        return self.connect()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Type[BaseException]],
    ) -> None:
        """Close the Redis connection when exiting the context."""
        self.close()
