import os
from typing import Callable, Optional

from confluent_kafka import Consumer, KafkaException, Message
from dotenv import load_dotenv


class EventConsumer:
    _consumer: Consumer = None

    def __init__(self) -> None:
        load_dotenv()
        self._consumer = Consumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                "group.id": os.getenv("KAFKA_GROUP_ID"),
                "auto.offset.reset": "earliest",
            }
        )
        self._consumer.subscribe([os.getenv("KAFKA_TOPIC")])

    def consume(
        self,
        handler: Callable[[Message], None],
        limit: Optional[int] = None,
        timeout: float = 10.0,
    ) -> int:
        """Consumes messages until `limit` is reached (forever if None)."""
        count = 0
        while limit is None or count < limit:
            # poll returns None if no message is received before the timeout
            message = self._consumer.poll(timeout)

            if message is None:
                if limit is None:
                    continue
                break

            if message.error():
                raise KafkaException(message.error())

            handler(message)
            count += 1

        return count

    def close(self) -> None:
        self._consumer.close()
