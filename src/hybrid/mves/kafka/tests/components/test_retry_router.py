import os

from confluent_kafka import Message

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer
from src.components.retry_router import RetryRouter


def first_message(topic: str) -> Message:
    received: list[Message] = []
    consumer = EventConsumer(topic, os.getenv("KAFKA_GROUP_ID"))
    consumer.consume(received.append, limit=1)
    consumer.close()
    return received[0]


def test_transient_error_goes_to_retry(topic):
    producer = EventProducer()
    producer.publish(topic, "madrid", {"trip_id": "trip-1"})
    producer.flush()

    target = RetryRouter(producer).route(
        first_message(topic), ConnectionError()
    )

    retried = first_message(target)
    assert target == os.getenv("KAFKA_RETRY_TOPIC")
    assert dict(retried.headers())["attempts"] == b"1"


def test_invalid_trip_goes_to_dlq(topic):
    producer = EventProducer()
    producer.publish(topic, "madrid", {"trip_id": "trip-1"})
    producer.flush()

    target = RetryRouter(producer).route(first_message(topic), ValueError())

    assert target == os.getenv("KAFKA_DLQ_TOPIC")
    assert b"ValueError" in dict(first_message(target).headers())["error"]


def test_exhausted_retries_go_to_dlq(topic):
    producer = EventProducer()
    attempts = str(int(os.getenv("MAX_ATTEMPTS")) - 1)
    producer.publish(
        topic, "madrid", {"trip_id": "trip-1"}, {"attempts": attempts}
    )
    producer.flush()

    target = RetryRouter(producer).route(
        first_message(topic), ConnectionError()
    )

    assert target == os.getenv("KAFKA_DLQ_TOPIC")
