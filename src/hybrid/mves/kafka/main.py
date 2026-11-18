import argparse
import time
from collections import Counter
from typing import Optional

from confluent_kafka import Message
from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

load_dotenv()

CITIES = ["madrid", "barcelona", "lisboa"]


def publish_trips(count: int, interval: float, flush: bool) -> None:
    """Publishes trips and reports how many were delivered or failed."""
    # With an interval the run is slow enough to follow every delivery
    producer = EventProducer(verbose=interval > 0)
    produced = Counter()
    start = time.perf_counter()

    print("--- Producing trips ---")
    try:
        for number in range(count):
            city = CITIES[number % len(CITIES)]
            producer.publish(city, f"trip-{number}")
            produced[city] += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n✓ Stopped producing")
    finally:
        # Without flush, events still in the local buffer are never sent
        pending = producer.flush() if flush else producer.pending
        elapsed = time.perf_counter() - start
        total = sum(produced.values())
        print(f"✓ Queued {total} trips: {dict(produced)}")
        print(f"✓ Delivered {producer.delivered}, "
              f"failed {sum(producer.failed.values())} {dict(producer.failed)}, "
              f"never sent {pending}")
        print(f"✓ {producer.delivered / elapsed:.0f} trips/s in {elapsed:.2f}s")


def consume_trips(limit: Optional[int] = None) -> None:
    """Consumes trips and reports how many unique trips arrived."""
    consumer = EventConsumer()
    seen = Counter()

    def process_trip(message: Message) -> None:
        city = message.key().decode()
        trip = message.value().decode()
        seen[trip] += 1
        print(f"✓ [partition {message.partition()}] {city} -> {trip}")

    print("\n--- Consuming trips ---")
    try:
        consumer.consume(process_trip, limit=limit)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()
        duplicates = sum(seen.values()) - len(seen)
        print(f"✓ Consumed {len(seen)} unique trips ({duplicates} duplicates)")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Only publish trips")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Only consume trips")
    parser.add_argument("-n", "--count", type=int, default=10,
                        help="Number of trips to publish")
    parser.add_argument("--interval", type=float, default=0,
                        help="Seconds between two published trips")
    parser.add_argument("--no-flush", action="store_true",
                        help="Exit without flushing the producer buffer")
    args = parser.parse_args()

    if not args.consume:
        publish_trips(args.count, args.interval, flush=not args.no_flush)

    if not args.publish:
        consume_trips(limit=None if args.consume else args.count)


if __name__ == "__main__":
    main()
