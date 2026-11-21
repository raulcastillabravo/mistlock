import argparse
import json
import os
import random
import time

from confluent_kafka import Message
from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer
from src.components.pricing import Pricing
from src.components.retry_router import RetryRouter
from src.components.trip_store import TripStore

load_dotenv()

CITIES = ["madrid", "barcelona", "lisboa"]


def publish_trips(count: int, invalid: int) -> None:
    """Publishes trips, the last `invalid` ones with a distance of 0."""
    producer = EventProducer()
    topic = os.getenv("KAFKA_TOPIC")
    start = time.perf_counter()

    for number in range(count + invalid):
        trip = {
            "trip_id": f"trip-{number}",
            "city": CITIES[number % len(CITIES)],
            "distance_km": round(random.uniform(1, 25), 1),
        }
        if number >= count:
            trip["distance_km"] = 0
        producer.publish(topic, trip["city"], trip)
    producer.flush()

    elapsed = time.perf_counter() - start
    print(f"✓ Produced {count + invalid} trips "
          f"({invalid} invalid) at {(count + invalid) / elapsed:.0f} trips/s")


def price_trips(
    topic: str, group: str, retrying: bool, stop_idle: bool = False
) -> None:
    """Prices the trips of `topic`, routing the failures."""
    pricing = Pricing()
    store = TripStore()
    router = RetryRouter(EventProducer())
    consumer = EventConsumer(topic, group)

    def process(message: Message) -> None:
        if retrying:
            RetryRouter.wait_for_turn(message)
        trip = json.loads(message.value())
        try:
            fare = pricing.fare(trip)
        except (ConnectionError, ValueError) as error:
            target = router.route(message, error)
            print(f"✗ {trip['trip_id']}: {error!r} -> {target}")
            return
        store.save(trip["trip_id"], trip["city"], fare)
        print(f"✓ {trip['trip_id']}: {fare:.2f} €")

    print(f"--- Pricing trips from {topic} ---")
    try:
        consumer.consume(process, stop_idle=stop_idle)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def redrive() -> None:
    """Sends every event in the DLQ back to the main topic."""
    producer = EventProducer()
    topic = os.getenv("KAFKA_TOPIC")
    consumer = EventConsumer(os.getenv("KAFKA_DLQ_TOPIC"), "redrive")

    def resend(message: Message) -> None:
        producer.publish(topic, message.key(), json.loads(message.value()))
        producer.flush()
        print(f"✓ Redriven: {json.loads(message.value())['trip_id']}")

    count = consumer.consume(resend, limit=None, timeout=5.0, stop_idle=True)
    consumer.close()
    print(f"✓ Redriven {count} events to {topic}")


def report() -> None:
    count, total = TripStore().summary()
    print(f"✓ {count} trips priced, {total:.2f} € in total")


def main() -> None:
    parser = argparse.ArgumentParser()
    # Without a mode it publishes the trips, prices them and reports
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Publish trips")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Price the trips of the main topic")
    mode.add_argument("-r", "--retry", action="store_true",
                      help="Price the trips of the retry topic")
    mode.add_argument("--redrive", action="store_true",
                      help="Send the DLQ events back to the main topic")
    mode.add_argument("--report", action="store_true",
                      help="Show how many trips are priced and their total")
    parser.add_argument("-n", "--count", type=int, default=10,
                        help="Number of valid trips to publish")
    parser.add_argument("--invalid", type=int, default=0,
                        help="Number of invalid trips to publish")
    args = parser.parse_args()

    group = os.getenv("KAFKA_GROUP_ID")
    if args.publish:
        publish_trips(args.count, args.invalid)
    elif args.consume:
        price_trips(os.getenv("KAFKA_TOPIC"), group, retrying=False)
    elif args.retry:
        price_trips(os.getenv("KAFKA_RETRY_TOPIC"), f"{group}.retry",
                    retrying=True)
    elif args.redrive:
        redrive()
    elif args.report:
        report()
    else:
        publish_trips(args.count, args.invalid)
        price_trips(os.getenv("KAFKA_TOPIC"), group, retrying=False,
                    stop_idle=True)
        report()


if __name__ == "__main__":
    main()
