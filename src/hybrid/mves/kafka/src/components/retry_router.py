import json
import os
import time

from confluent_kafka import Message

from src.components.event_producer import EventProducer


class RetryRouter:
    """Sends a failed event to the retry topic or, when retrying cannot
    help or the attempts run out, to the DLQ."""

    _producer: EventProducer = None
    _retry_topic: str = None
    _dlq_topic: str = None
    _max_attempts: int = None
    _backoff: float = None

    def __init__(self, producer: EventProducer) -> None:
        self._producer = producer
        self._retry_topic = os.getenv("KAFKA_RETRY_TOPIC")
        self._dlq_topic = os.getenv("KAFKA_DLQ_TOPIC")
        self._max_attempts = int(os.getenv("MAX_ATTEMPTS"))
        self._backoff = float(os.getenv("RETRY_BACKOFF_SECONDS"))

    def route(self, message: Message, error: Exception) -> str:
        """Publishes the event to its next topic and returns that topic."""
        headers = dict(message.headers() or [])
        attempts = int(headers.get("attempts", b"0")) + 1
        trip = json.loads(message.value())

        if isinstance(error, ConnectionError) and attempts < self._max_attempts:
            # Exponential backoff: 2 s, 4 s, 8 s...
            delay = self._backoff * 2 ** (attempts - 1)
            topic = self._retry_topic
            headers = {
                "attempts": str(attempts),
                "not_before": str(time.time() + delay),
            }
        else:
            topic = self._dlq_topic
            headers = {
                "attempts": str(attempts),
                "error": repr(error),
                "source": f"{message.topic()}/{message.partition()}"
                          f"/{message.offset()}",
            }

        self._producer.publish(topic, message.key(), trip, headers)
        # The event must be safe in its next topic before the caller
        # commits the offset, or a crash in between would lose it
        self._producer.flush()
        return topic

    @staticmethod
    def wait_for_turn(message: Message) -> None:
        """Sleeps until the backoff of a retried event has passed."""
        headers = dict(message.headers())
        time.sleep(max(0.0, float(headers["not_before"]) - time.time()))
