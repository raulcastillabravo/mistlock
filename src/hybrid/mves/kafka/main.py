import argparse
import os
import random
from typing import Optional

from confluent_kafka import Message
from dotenv import load_dotenv

from src.components.event_consumer import EventConsumer
from src.components.event_producer import EventProducer

load_dotenv()

EVENTS = [
    ("john@example.com", "user-registered"),
    ("carol@example.com", "user-logged-in"),
    ("eve@example.com", "user-updated"),
]


def publish_event() -> None:
    key, value = random.choice(EVENTS)
    EventProducer().publish(key, value)
    print(f"✓ Produced: {key} -> {value}")


def consume_events(
    group: Optional[int], offset_reset: str, limit: Optional[int] = None
) -> None:
    group_id = os.getenv("KAFKA_GROUP_ID")
    if group:
        group_id = f"{group_id}-{group}"
    consumer = EventConsumer(group_id, offset_reset)

    print(f"\n--- Consuming events as {group_id} ({offset_reset}) ---")
    try:
        consumer.consume(HANDLERS[group], limit=limit)
    except KeyboardInterrupt:
        print("\n✓ Stopped consuming")
    finally:
        consumer.close()


def print_event(message: Message) -> None:
    print(f"✓ Consumed: {describe(message)}")


def handle_group_1(message: Message) -> None:
    print(f"✓ I am group 1, consumed: {describe(message)}")


def handle_group_2(message: Message) -> None:
    print(f"✓ I am group 2, consumed: {describe(message)}")


def describe(message: Message) -> str:
    key = message.key().decode()
    value = message.value().decode()
    return f"{key} -> {value} [partition {message.partition()}]"


HANDLERS = {None: print_event, 1: handle_group_1, 2: handle_group_2}


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-p", "--publish", action="store_true",
                      help="Only publish one event")
    mode.add_argument("-c", "--consume", action="store_true",
                      help="Only consume events")
    parser.add_argument("-g", "--consumer-group", type=int, choices=[1, 2],
                        help="Consumer group that runs its own logic")
    parser.add_argument("-o", "--offset-reset", default="earliest",
                        choices=["earliest", "latest"],
                        help="Where a new group starts reading the topic")
    args = parser.parse_args()

    if not args.consume:
        publish_event()

    if not args.publish:
        consume_events(
            args.consumer_group,
            args.offset_reset,
            limit=None if args.consume else 1,
        )


if __name__ == "__main__":
    main()
