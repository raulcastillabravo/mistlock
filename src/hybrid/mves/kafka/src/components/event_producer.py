import json
import os
from typing import Optional

from confluent_kafka import Producer

# Throughput settings read from the environment. Unset variables keep the
# client default, so the lab shows what changes when each one is set.
SETTINGS = {
    "linger.ms": "KAFKA_LINGER_MS",
    "compression.type": "KAFKA_COMPRESSION_TYPE",
}


class EventProducer:
    _producer: Producer = None

    def __init__(self) -> None:
        config = {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
        for setting, variable in SETTINGS.items():
            if os.getenv(variable):
                config[setting] = os.getenv(variable)
        self._producer = Producer(config)

    def publish(
        self,
        topic: str,
        key: str,
        value: dict,
        headers: Optional[dict] = None,
    ) -> None:
        self._producer.produce(
            topic, key=key, value=json.dumps(value), headers=headers
        )
        # Serves delivery reports so the local buffer does not fill up
        self._producer.poll(0)

    def flush(self) -> None:
        self._producer.flush()
