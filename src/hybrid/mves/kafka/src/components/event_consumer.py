import os
from typing import Callable, Optional

from confluent_kafka import (
    Consumer,
    KafkaError,
    KafkaException,
    Message,
    TopicPartition,
)
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
                "partition.assignment.strategy": os.getenv(
                    "KAFKA_ASSIGNMENT_STRATEGY"
                ),
                "session.timeout.ms": os.getenv("KAFKA_SESSION_TIMEOUT_MS"),
                "max.poll.interval.ms": os.getenv(
                    "KAFKA_MAX_POLL_INTERVAL_MS"
                ),
            }
        )
        self._consumer.subscribe(
            [os.getenv("KAFKA_TOPIC")],
            on_assign=self._on_assign,
            on_revoke=self._on_revoke,
        )

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
                # Too slow between polls: the group kicked us out, but the
                # consumer rejoins on the next poll.
                if message.error().code() == KafkaError._MAX_POLL_EXCEEDED:
                    print(f"⚠ {message.error().str()}")
                    continue
                raise KafkaException(message.error())

            handler(message)
            count += 1

        return count

    def close(self) -> None:
        self._consumer.close()

    def _on_assign(
        self, consumer: Consumer, partitions: list[TopicPartition]
    ) -> None:
        print(f"⇢ Assigned partitions: {[p.partition for p in partitions]}")

    def _on_revoke(
        self, consumer: Consumer, partitions: list[TopicPartition]
    ) -> None:
        print(f"⇠ Revoked partitions: {[p.partition for p in partitions]}")
