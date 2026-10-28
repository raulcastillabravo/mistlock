import argparse
import time
from typing import Optional

from confluent_kafka import Message
from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

load_dotenv()

EVENTS = [
    ("user-registered", "john@example.com"),
    ("user-logged-in", "jane@example.com"),
    ("user-updated", "bob@example.com"),
]


def publish_events() -> None:
    producer = EventProducer()

    print("--- Producing events ---")
    for key, value in EVENTS:
        producer.publish(key, value)
        print(f"✓ Produced: {key} -> {value}")


def consume_events(commit: str, limit: Optional[int] = None) -> None:
    consumer = EventConsumer(commit)

    print(f"\n--- Consuming events (commit: {commit}) ---")
    try:
        consumer.consume(process_event, limit=limit)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def process_event(message: Message) -> None:
    """Simulates a slow side effect (e.g. a database write)."""
    key = message.key().decode()
    print(f"… Processing offset {message.offset()}: {key}")
    # Seconds each event takes. Change it to reproduce each scenario:
    # 0 to see duplicates, above the 5s auto commit interval (e.g. 10)
    # to see a lost event.
    time.sleep(10)
    print(f"✓ Processed offset {message.offset()}: {key}")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Only publish events")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Only consume events")
    parser.add_argument("--commit", default="auto",
                        choices=["auto", "before", "after"],
                        help="When the consumer commits its offset")
    args = parser.parse_args()

    if not args.consume:
        publish_events()

    if not args.publish:
        consume_events(
            args.commit,
            limit=None if args.consume else len(EVENTS),
        )


if __name__ == "__main__":
    main()
