from confluent_kafka import Message
from dotenv import load_dotenv

from src.providers.event_consumer import EventConsumer
from src.providers.event_producer import EventProducer

load_dotenv()

EVENTS = [
    ("user-registered", "john@example.com"),
    ("user-logged-in", "jane@example.com"),
    ("user-updated", "bob@example.com"),
]


def print_event(message: Message) -> None:
    key = message.key().decode()
    value = message.value().decode()
    print(f"✓ Consumed: {key} -> {value}")


def main() -> None:
    producer = EventProducer()

    print("--- Producing events ---")
    for key, value in EVENTS:
        producer.publish(key, value)
        print(f"✓ Produced: {key} -> {value}")

    print("\n--- Consuming events ---")
    consumer = EventConsumer()
    consumer.consume(print_event, limit=len(EVENTS))
    consumer.close()

    print("\n✓ Done! You can verify the events in the Kafka UI.")


if __name__ == "__main__":
    main()
