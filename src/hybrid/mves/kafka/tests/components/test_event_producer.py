import json
import os

from confluent_kafka import Message

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer


def test_event_producer(topic):
    producer = EventProducer()
    producer.publish(topic, "madrid", {"trip_id": "trip-1"}, {"attempts": "1"})
    producer.flush()

    received: list[Message] = []
    consumer = EventConsumer(topic, os.getenv("KAFKA_GROUP_ID"))
    consumer.consume(received.append, limit=1)
    consumer.close()

    assert len(received) == 1
    assert received[0].key().decode() == "madrid"
    assert json.loads(received[0].value()) == {"trip_id": "trip-1"}
    assert dict(received[0].headers()) == {"attempts": b"1"}
