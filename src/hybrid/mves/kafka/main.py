import argparse
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


def consume_events(limit: Optional[int] = None) -> None:
    consumer = EventConsumer()

    print("\n--- Consuming events ---")
    try:
        consumer.consume(print_event, limit=limit)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def print_event(message: Message) -> None:
    key = message.key().decode()
    value = message.value().decode()
    print(f"✓ Consumed: {key} -> {value}")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Only publish events")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Only consume events")
    args = parser.parse_args()

    if not args.consume:
        publish_events()

    if not args.publish:
        consume_events(limit=None if args.consume else len(EVENTS))


if __name__ == "__main__":
    main()
