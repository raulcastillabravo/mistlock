import os
from io import BytesIO

from confluent_kafka import Producer
from fastavro import schemaless_writer

from src.components.schema_catalog import SchemaCatalog


class EventProducer:
    _topic: str = None
    _producer: Producer = None
    _version: int = None
    _schema: dict = None

    def __init__(self, version: int) -> None:
        """Publishes events serialized with Avro using schema `version`."""
        self._topic = os.getenv("KAFKA_TOPIC")
        self._producer = Producer(
            {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
        )
        self._version = version
        self._schema = SchemaCatalog().load(version)

    def publish(self, key: str, value: dict) -> int:
        """Publishes the event and returns its size in bytes.

        Avro bytes carry no field names, so the schema version travels in a
        header: without it the consumer could not decode the event.
        """
        buffer = BytesIO()
        schemaless_writer(buffer, self._schema, value)
        payload = buffer.getvalue()
        self._producer.produce(
            self._topic,
            key=key,
            value=payload,
            headers={"schema_version": str(self._version)},
        )
        return len(payload)

    def flush(self) -> None:
        self._producer.flush()
