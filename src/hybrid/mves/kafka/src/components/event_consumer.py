import os
from io import BytesIO
from typing import Callable, Optional

from confluent_kafka import Consumer, KafkaException, Message
from fastavro import schemaless_reader

from src.components.schema_catalog import SchemaCatalog


class EventConsumer:
    _consumer: Consumer = None
    _catalog: SchemaCatalog = None
    _reader: dict = None

    def __init__(self, version: int) -> None:
        """Reads events into the shape of schema `version`.

        Each event is decoded with the schema it was written with (its
        header) and Avro resolves it into the reader schema: unknown fields
        are dropped and missing ones take their default.
        """
        self._consumer = Consumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                "group.id": os.getenv("KAFKA_GROUP_ID"),
                "auto.offset.reset": "earliest",
            }
        )
        self._consumer.subscribe([os.getenv("KAFKA_TOPIC")])
        self._catalog = SchemaCatalog()
        self._reader = self._catalog.load(version)

    def consume(
        self,
        handler: Callable[[dict], None],
        limit: Optional[int] = None,
        timeout: float = 10.0,
    ) -> int:
        """Consumes events until `limit` is reached (forever if None)."""
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

            handler(self._decode(message))
            count += 1

        return count

    def close(self) -> None:
        self._consumer.close()

    def _decode(self, message: Message) -> dict:
        headers = dict(message.headers())
        writer = self._catalog.load(int(headers["schema_version"]))
        return schemaless_reader(BytesIO(message.value()), writer, self._reader)
