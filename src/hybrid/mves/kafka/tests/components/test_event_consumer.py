import signal

from confluent_kafka import Message

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

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
    count = consumer.consume(fail_on_message, limit=1, timeout=5.0)
    consumer.close()

    assert count == 0


def test_event_consumer_stops_gracefully_on_sigint(topic):
    producer = EventProducer()
    for key, value in EVENTS:
        producer.publish(key, value)

    processed: list[Message] = []

    def interrupt_while_processing(message: Message) -> None:
        signal.raise_signal(signal.SIGINT)
        processed.append(message)

    consumer = EventConsumer()
    count = consumer.consume(interrupt_while_processing, limit=len(EVENTS))
    consumer.close()

    assert count == 1
    assert [m.key().decode() for m in processed] == [EVENTS[0][0]]


def fail_on_message(message: Message) -> None:
    raise AssertionError(f"Unexpected message: {message.key()}")
