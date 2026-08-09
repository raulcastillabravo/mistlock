import os

from confluent_kafka import Producer
from dotenv import load_dotenv


class EventProducer:
    _topic: str = None
    _producer: Producer = None

    def __init__(self) -> None:
        load_dotenv()
        self._topic = os.getenv("KAFKA_TOPIC")
        self._producer = Producer(
            {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
        )

    def publish(self, key: str, value: str) -> None:
        self._producer.produce(self._topic, key=key, value=value)
        self._producer.flush()
