import argparse
import random
import time
from collections import Counter
from functools import partial
from typing import Optional

from confluent_kafka import Message
from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

load_dotenv()

# Madrid generates most trips, so its partition becomes a hot partition.
# Each key maps to a different partition when the topic has 3 partitions.
CITIES = {"madrid": 70, "barcelona": 20, "lisboa": 10}


def publish_trips(count: int) -> None:
    producer = EventProducer()
    cities = random.choices(list(CITIES), weights=CITIES.values(), k=count)

    for number, city in enumerate(cities):
        producer.publish(city, f"trip-{number}")
    print(f"✓ Produced {count} trips: {dict(Counter(cities))}")


def consume_trips(delay: float, limit: Optional[int] = None) -> None:
    consumer = EventConsumer()

    print("\n--- Consuming trips ---")
    try:
        consumer.consume(partial(process_trip, delay=delay), limit=limit)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def process_trip(message: Message, delay: float) -> None:
    """Simulates the time each trip takes to be processed."""
    time.sleep(delay)
    city = message.key().decode()
    trip = message.value().decode()
    print(f"✓ [partition {message.partition()}] {city} -> {trip}")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Only publish trips")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Only consume trips")
    parser.add_argument("-n", "--count", type=int, default=10,
                        help="Number of trips to publish")
    parser.add_argument("--delay", type=float, default=0,
                        help="Seconds each trip takes to be processed")
    args = parser.parse_args()

    if not args.consume:
        publish_trips(args.count)

    if not args.publish:
        consume_trips(args.delay, limit=None if args.consume else args.count)


if __name__ == "__main__":
    main()
