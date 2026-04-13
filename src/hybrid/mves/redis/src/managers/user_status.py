from enum import Enum
from typing import Optional

from src.providers.redis_client import RedisClient


class Status(Enum):
    INACTIVE = "inactive"
    AVAILABLE = "available"
    BUSY = "busy"


class UserStatus:
    _username: str = None

    def __init__(self, username: str) -> None:
        self._username = username

    def set_status(self, status: Status) -> None:
        with RedisClient() as client:
            client.set(f"{self._username}:status", status.value)

    def get_status(self) -> Optional[Status]:
        with RedisClient() as client:
            value = client.get(f"{self._username}:status")
            return Status(value) if value else None
