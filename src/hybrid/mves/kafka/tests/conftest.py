import os
import time

import pytest
from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.test", override=True)


def delete_topic(admin: AdminClient, name: str) -> None:
    """Deletes the topic, ignoring it when it does not exist."""
    for future in admin.delete_topics([name]).values():
        try:
            future.result()
        except KafkaException as error:
            if error.args[0].code() != KafkaError.UNKNOWN_TOPIC_OR_PART:
                raise


def wait_for_topic(admin: AdminClient, name: str) -> None:
    """Waits until the broker metadata lists the topic."""
    deadline = time.monotonic() + 10
    while name not in admin.list_topics(timeout=5).topics:
        assert time.monotonic() < deadline, f"Topic {name} not ready"
        time.sleep(0.2)


@pytest.fixture
def topic() -> str:
    """Creates the main, retry and DLQ topics per test and removes them
    afterwards. Yields the main one."""
    admin = AdminClient(
        {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
    )
    names = [
        os.getenv("KAFKA_TOPIC"),
        os.getenv("KAFKA_RETRY_TOPIC"),
        os.getenv("KAFKA_DLQ_TOPIC"),
    ]

    for name in names:
        delete_topic(admin, name)

    topics = [NewTopic(name, 1, 1) for name in names]
    for future in admin.create_topics(topics).values():
        future.result()

    for name in names:
        wait_for_topic(admin, name)

    yield names[0]

    for name in names:
        delete_topic(admin, name)


@pytest.fixture
def store_path(tmp_path, monkeypatch) -> str:
    """Points the trip store to a throwaway SQLite file."""
    path = str(tmp_path / "trips.sqlite3")
    monkeypatch.setenv("TRIP_STORE_PATH", path)
    return path
