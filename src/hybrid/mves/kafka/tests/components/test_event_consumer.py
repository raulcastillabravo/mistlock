from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

TRIP_V2 = {
    "trip_id": "trip-1",
    "city": "madrid",
    "driver_id": "driver-1",
    "distance_km": 3.5,
    "amount": 12.4,
    "payment_method": "card",
}


def test_event_consumer_reads_newer_schema(topic):
    producer = EventProducer(2)
    producer.publish("madrid", TRIP_V2)
    producer.flush()

    received: list[dict] = []
    consumer = EventConsumer(1)
    count = consumer.consume(received.append, limit=1)
    consumer.close()

    # A v1 reader drops the field it does not know
    assert count == 1
    assert "payment_method" not in received[0]
    assert received[0]["amount"] == TRIP_V2["amount"]


def test_event_consumer_stops_on_timeout(topic):
    consumer = EventConsumer(1)
    count = consumer.consume(fail_on_event, limit=1, timeout=5.0)
    consumer.close()

    assert count == 0


def fail_on_event(event: dict) -> None:
    raise AssertionError(f"Unexpected event: {event}")
