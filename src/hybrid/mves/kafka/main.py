import argparse
import json
import os
import random
from typing import Optional

from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer
from src.components.schema_catalog import SchemaCatalog

load_dotenv()

CITIES = ["madrid", "barcelona", "lisboa"]
PAYMENT_METHODS = ["card", "cash", "wallet"]


def build_trip(number: int) -> dict:
    """Builds a trip with every field any schema version may ask for.

    Avro writes only the fields of the producer schema and skips the rest.
    """
    amount = round(random.uniform(5, 40), 2)
    return {
        "trip_id": f"trip-{number}",
        "city": CITIES[number % len(CITIES)],
        "driver_id": f"driver-{random.randint(1, 20)}",
        "distance_km": round(random.uniform(1, 25), 1),
        "amount": amount,
        "fare": amount,
        "payment_method": random.choice(PAYMENT_METHODS),
    }


def publish_trips(count: int, version: int) -> None:
    """Publishes trips and compares the Avro size with the JSON size."""
    producer = EventProducer(version)
    fields = [f["name"] for f in SchemaCatalog().load(version)["fields"]]
    avro_bytes = 0
    json_bytes = 0

    print(f"--- Producing trips with schema v{version} ---")
    for number in range(count):
        trip = build_trip(number)
        avro_bytes += producer.publish(trip["city"], trip)
        written = {name: trip[name] for name in fields}
        json_bytes += len(json.dumps(written).encode())
        print(f"✓ Produced: {trip['trip_id']}")
    producer.flush()

    print(f"✓ Avro: {avro_bytes / count:.0f} bytes/trip, "
          f"JSON: {json_bytes / count:.0f} bytes/trip")


def consume_trips(version: int, limit: Optional[int] = None) -> None:
    consumer = EventConsumer(version)

    print(f"\n--- Consuming trips with schema v{version} ---")
    try:
        consumer.consume(lambda trip: print(f"✓ Consumed: {trip}"), limit)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Only publish trips")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Only consume trips")
    parser.add_argument("-n", "--count", type=int, default=3,
                        help="Number of trips to publish")
    parser.add_argument("-s", "--schema", type=int,
                        default=int(os.environ["TRIP_SCHEMA_VERSION"]),
                        help="Schema version to write or read trips with")
    args = parser.parse_args()

    if not args.consume:
        publish_trips(args.count, args.schema)

    if not args.publish:
        limit = None if args.consume else args.count
        consume_trips(args.schema, limit)


if __name__ == "__main__":
    main()
