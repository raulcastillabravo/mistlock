from confluent_kafka import Message
from dotenv import load_dotenv

from src.providers.event_consumer import EventConsumer

load_dotenv()


def print_event(message: Message) -> None:
    print(f"✓ Consumed: {message.key().decode()} -> {message.value().decode()}")


def main() -> None:
    consumer = EventConsumer()
    print("--- Listening for events. Press CTRL+C to exit ---")

    try:
        consumer.consume(print_event)
    except KeyboardInterrupt:
        print("\n✓ Stopped listening")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
