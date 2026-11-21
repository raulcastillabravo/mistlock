import os

from confluent_kafka import Message

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

TRIPS = [{"trip_id": "trip-1"}, {"trip_id": "trip-2"}]


def test_event_consumer(topic):
    producer = EventProducer()
    for trip in TRIPS:
        producer.publish(topic, "madrid", trip)
    producer.flush()

    received: list[Message] = []
    consumer = EventConsumer(topic, os.getenv("KAFKA_GROUP_ID"))
    count = consumer.consume(received.append, limit=len(TRIPS))
    consumer.close()

    assert count == len(TRIPS)


def test_event_consumer_stops_when_idle(topic):
    consumer = EventConsumer(topic, os.getenv("KAFKA_GROUP_ID"))
    count = consumer.consume(fail_on_message, timeout=5.0, stop_idle=True)
    consumer.close()

    assert count == 0


def fail_on_message(message: Message) -> None:
    raise AssertionError(f"Unexpected message: {message.key()}")
