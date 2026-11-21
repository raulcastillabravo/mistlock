import os
from typing import Callable, Optional

from confluent_kafka import Consumer, KafkaError, KafkaException, Message


class EventConsumer:
    _consumer: Consumer = None

    def __init__(self, topic: str, group: str) -> None:
        self._consumer = Consumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                "group.id": group,
                "auto.offset.reset": "earliest",
                # At-least-once: commit only after the handler finished
                "enable.auto.commit": False,
            }
        )
        self._consumer.subscribe([topic])

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
            # The retry and DLQ topics only exist after the first failure
            if error and error.code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                continue
            if error:
                raise KafkaException(error)

            handler(message)
            self._consumer.commit(message, asynchronous=False)
            count += 1

        return count

    def close(self) -> None:
        self._consumer.close()
