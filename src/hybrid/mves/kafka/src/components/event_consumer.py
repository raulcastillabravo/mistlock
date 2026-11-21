import os
from typing import Callable, Optional

from confluent_kafka import Consumer, KafkaError, KafkaException, Message


class EventConsumer:
    _consumer: Consumer = None

    def __init__(self, group: str) -> None:
        self._consumer = Consumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                "group.id": group,
                "auto.offset.reset": "earliest",
            }
        )
        self._consumer.subscribe([os.getenv("KAFKA_TOPIC")])

    def consume(
        self,
        handler: Callable[[Message], None],
        limit: Optional[int] = None,
        timeout: float = 10.0,
        stop_idle: bool = False,
    ) -> int:
        """Consumes messages until `limit` is reached (forever if None).

        With `stop_idle` it also stops when no message arrives in `timeout`.
        """
        count = 0
        while limit is None or count < limit:
            # poll returns None if no message is received before the timeout
            message = self._consumer.poll(timeout)

            if message is None:
                if limit is None and not stop_idle:
                    continue
                break

            error = message.error()
            # Debezium creates the topic with the first event it publishes
            if error and error.code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                continue
            if error:
                raise KafkaException(error)

            handler(message)
            count += 1

        return count

    def close(self) -> None:
        self._consumer.close()
