import os
import signal
from typing import Callable, Optional

from confluent_kafka import Consumer, KafkaException, Message
from dotenv import load_dotenv

# Short polls keep the loop responsive to a shutdown request
POLL_INTERVAL = 1.0


class EventConsumer:
    _consumer: Consumer = None
    _running: bool = False

    def __init__(self) -> None:
        load_dotenv()
        self._consumer = Consumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                "group.id": os.getenv("KAFKA_GROUP_ID"),
                "auto.offset.reset": "earliest",
            }
        )
        self._consumer.subscribe([os.getenv("KAFKA_TOPIC")])

    def consume(
        self,
        handler: Callable[[Message], None],
        limit: Optional[int] = None,
        timeout: float = 10.0,
    ) -> int:
        """Consumes messages until `limit` is reached (forever if None).

        On SIGINT, the event in progress is finished before stopping.
        """
        self._running = True
        previous_handler = signal.signal(signal.SIGINT, self._stop)
        try:
            return self._consume_loop(handler, limit, timeout)
        finally:
            signal.signal(signal.SIGINT, previous_handler)

    def _consume_loop(
        self,
        handler: Callable[[Message], None],
        limit: Optional[int],
        timeout: float,
    ) -> int:
        count = 0
        idle = 0.0
        while self._running and (limit is None or count < limit):
            # poll returns None if no message is received before the interval
            message = self._consumer.poll(POLL_INTERVAL)

            if message is None:
                idle += POLL_INTERVAL
                if limit is not None and idle >= timeout:
                    break
                continue

            if message.error():
                raise KafkaException(message.error())

            handler(message)
            count += 1
            idle = 0.0

        return count

    def _stop(self, signum: int, frame: object) -> None:
        print("\n✓ SIGINT received, stopping after the current event")
        self._running = False
        # A second Ctrl+C forces an immediate exit
        signal.signal(signal.SIGINT, signal.default_int_handler)

    def close(self) -> None:
        self._consumer.close()
