import redis
import os
from dotenv import load_dotenv

load_dotenv()

class RedisClient:

    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.password = os.getenv('REDIS_PASSWORD')
        self.client = None
    
    def connect(self) -> redis.Redis:
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=True
        )
        return self.client

    def close(self):
        if self.client:
            self.client.close()