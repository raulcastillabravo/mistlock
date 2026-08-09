from confluent_kafka import Message

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer


def test_event_producer(topic):
    producer = EventProducer()
    producer.publish("test-event", "test@example.com")

    received: list[Message] = []
    consumer = EventConsumer()
    consumer.consume(received.append, limit=1)
    consumer.close()

    assert len(received) == 1
    assert received[0].key().decode() == "test-event"
    assert received[0].value().decode() == "test@example.com"
