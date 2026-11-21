import argparse
import json
import os
import random
import uuid
from typing import Optional

from confluent_kafka import Message
from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer
from src.components.trip_repository import TripRepository

load_dotenv()

CITIES = ["madrid", "barcelona", "lisboa"]


def build_trip() -> dict:
    return {
        "trip_id": f"trip-{uuid.uuid4().hex[:8]}",
        "city": random.choice(CITIES),
        "distance_km": round(random.uniform(1, 25), 1),
    }


def dual_write(count: int, crash_at: Optional[int]) -> None:
    """Saves each trip in Postgres and then publishes it to Kafka: two
    separate writes, with nothing that keeps them together."""
    repository = TripRepository()
    producer = EventProducer()

    for number in range(count):
        trip = build_trip()
        with repository.transaction():
            repository.insert_trip(trip)
        print(f"✓ Saved {trip['trip_id']} in Postgres")

        if number == crash_at:
            print("💥 Crash between the two writes")
            os._exit(1)

        producer.publish(trip["trip_id"], json.dumps(trip))
        print(f"✓ Published {trip['trip_id']} to Kafka")


def outbox(count: int, crash_at: Optional[int]) -> None:
    """Saves each trip and its event in one transaction. Debezium publishes
    the event later, reading the outbox table from the WAL."""
    repository = TripRepository()

    for number in range(count):
        trip = build_trip()
        with repository.transaction():
            repository.insert_trip(trip)
            repository.insert_event(trip)
            if number == crash_at:
                print("💥 Crash before the commit")
                os._exit(1)
        print(f"✓ Saved {trip['trip_id']} and its event in Postgres")


def consume() -> None:
    consumer = EventConsumer(os.getenv("KAFKA_GROUP_ID"))

    def print_trip(message: Message) -> None:
        headers = dict(message.headers() or [])
        print(f"✓ {message.value().decode()} {headers}")

    print("--- Consuming trips ---")
    try:
        consumer.consume(print_trip)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def check() -> None:
    """Compares the trips in Postgres with the events in Kafka."""
    published: set[str] = set()
    # A new group reads the whole topic from the start
    consumer = EventConsumer(f"check-{uuid.uuid4().hex[:8]}")
    consumer.consume(
        lambda message: published.add(json.loads(message.value())["trip_id"]),
        timeout=5.0,
        stop_idle=True,
    )
    consumer.close()

    saved = TripRepository().trip_ids()
    missing = sorted(saved - published)
    print(f"✓ {len(saved)} trips in Postgres, {len(published)} in Kafka")
    print(f"{'✗' if missing else '✓'} Without event: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dual-write", action="store_true",
                      help="Save in Postgres, then publish to Kafka")
    mode.add_argument("--outbox", action="store_true",
                      help="Save the trip and its event in one transaction")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Consume the trips topic")
    mode.add_argument("--check", action="store_true",
                      help="Find trips in Postgres without an event")
    parser.add_argument("-n", "--count", type=int, default=3,
                        help="Number of trips to create")
    parser.add_argument("--crash-at", type=int,
                        help="Kill the process while creating this trip")
    args = parser.parse_args()

    if args.outbox:
        outbox(args.count, args.crash_at)
    elif args.consume:
        consume()
    elif args.check:
        check()
    else:
        # Default: the dual write, which needs no connector
        dual_write(args.count, args.crash_at)
        check()


if __name__ == "__main__":
    main()
