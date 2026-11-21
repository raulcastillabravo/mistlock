from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

TRIP_V1 = {
    "trip_id": "trip-1",
    "city": "madrid",
    "driver_id": "driver-1",
    "distance_km": 3.5,
    "amount": 12.4,
}


def test_event_producer(topic):
    producer = EventProducer(1)
    producer.publish("madrid", TRIP_V1)
    producer.flush()

    received: list[dict] = []
    consumer = EventConsumer(1)
    consumer.consume(received.append, limit=1)
    consumer.close()

    assert received == [TRIP_V1]
