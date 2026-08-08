from confluent_kafka import Message

from src.providers.event_consumer import EventConsumer
from src.providers.event_producer import EventProducer

EVENTS = [("first", "a@example.com"), ("second", "b@example.com")]


def test_event_consumer(topic):
    producer = EventProducer()
    for key, value in EVENTS:
        producer.publish(key, value)

    received: list[Message] = []
    consumer = EventConsumer()
    count = consumer.consume(received.append, limit=len(EVENTS))
    consumer.close()

    assert count == len(EVENTS)
    assert [m.key().decode() for m in received] == [k for k, _ in EVENTS]


def test_event_consumer_stops_on_timeout(topic):
    consumer = EventConsumer()
    count = consumer.consume(received_none, limit=1, timeout=5.0)
    consumer.close()

    assert count == 0


def received_none(message: Message) -> None:
    raise AssertionError(f"Unexpected message: {message.key()}")
