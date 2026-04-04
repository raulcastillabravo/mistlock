import time
from contextlib import contextmanager
from redis_client import RedisClient
from typing import Generator


class LockAcquisitionError(Exception):
    """Raised when a lock cannot be acquired within the specified timeout."""
    pass


class RedisMutex(RedisClient):
    """Distributed mutex using Redis for coordinating access to shared resources."""

    def __init__(self):
        super().__init__()
        self.connect()

    def __enter__(self):
        """Context manager entry - returns self for use in with statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed."""
        self.close()
        return False  # Don't suppress exceptions

    def lock(self, resource: str, wait_sec: float = 10.0, retry_sec: float = 0.1) -> bool:
        """Acquire a lock on the resource. Returns True if successful, False if timeout."""
        lock_key = f"lock:{resource}"
        start_time = time.time()
        
        while True:
            if self.client.set(lock_key, "locked", nx=True, ex=30):
                return True
            
            if time.time() - start_time >= wait_sec:
                return False
            
            time.sleep(retry_sec)

    def unlock(self, resource: str):
        """Release the specified locked resource."""
        if resource:
            self.client.delete(f"lock:{resource}")

    @contextmanager
    def acquire(self, resource: str, wait_sec: float = 10.0, retry_sec: float = 0.1) -> Generator[None, None, None]:
        """Context manager for acquiring and automatically releasing a lock.
        
        Raises:
            LockAcquisitionError: If the lock cannot be acquired within wait_sec.
        """
        lock_acquired = False
        try:
            if not self.lock(resource, wait_sec, retry_sec):
                raise LockAcquisitionError(f"Could not acquire lock for '{resource}' after {wait_sec}s")
            lock_acquired = True
            yield
        finally:
            if lock_acquired:
                self.unlock(resource)

