import os
from collections import Counter
from typing import Optional

from confluent_kafka import KafkaError, Message, Producer
from dotenv import load_dotenv

# Producer settings read from the environment. Unset variables keep the
# client default, so the lab shows what changes when each one is set.
SETTINGS = {
    "acks": "KAFKA_ACKS",
    "enable.idempotence": "KAFKA_ENABLE_IDEMPOTENCE",
    "linger.ms": "KAFKA_LINGER_MS",
    "compression.type": "KAFKA_COMPRESSION_TYPE",
    "message.timeout.ms": "KAFKA_MESSAGE_TIMEOUT_MS",
    "retries": "KAFKA_RETRIES",
}


class EventProducer:
    _topic: str = None
    _producer: Producer = None

    def __init__(self, verbose: bool = False) -> None:
        load_dotenv()
        self._topic = os.getenv("KAFKA_TOPIC")
        self._verbose = verbose
        self.delivered = 0
        self.failed = Counter()

        config = {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
        for setting, variable in SETTINGS.items():
            if os.getenv(variable):
                config[setting] = os.getenv(variable)
        self._producer = Producer(config)

    def publish(self, key: str, value: str) -> None:
        """Queues the event. It is sent in the background, in batches."""
        self._producer.produce(
            self._topic, key=key, value=value, on_delivery=self._on_delivery
        )
        # Serves the delivery callbacks of events already sent
        self._producer.poll(0)

    def flush(self, timeout: Optional[float] = None) -> int:
        """Waits until every queued event is delivered or has failed.

        Returns the number of events still queued.
        """
        if timeout is None:
            return self._producer.flush()
        return self._producer.flush(timeout)

    @property
    def pending(self) -> int:
        """Events still in the local buffer, not yet delivered or failed."""
        return len(self._producer)

    def _on_delivery(self, error: Optional[KafkaError], message: Message) -> None:
        key = message.key().decode()
        value = message.value().decode()
        if error is not None:
            self.failed[error.name()] += 1
            print(f"✗ Failed: {key} -> {value} ({error.name()}: {error.str()})")
            return

        self.delivered += 1
        if self._verbose:
            print(f"✓ Delivered: {key} -> {value} "
                  f"[partition {message.partition()}, offset {message.offset()}]")
