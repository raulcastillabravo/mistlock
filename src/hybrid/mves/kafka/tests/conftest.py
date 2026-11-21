import os
import time
from pathlib import Path

import psycopg
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
    """Creates a dedicated topic per test and removes it afterwards."""
    admin = AdminClient(
        {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
    )
    name = os.getenv("KAFKA_TOPIC")

    delete_topic(admin, name)

    for future in admin.create_topics([NewTopic(name, 1, 1)]).values():
        future.result()

    wait_for_topic(admin, name)

    yield name

    delete_topic(admin, name)


@pytest.fixture
def database() -> str:
    """Recreates the test database with the lab schema."""
    name = os.getenv("POSTGRES_DB")
    settings = {
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
    }
    with psycopg.connect(dbname="postgres", autocommit=True, **settings) as admin:
        admin.execute(f"DROP DATABASE IF EXISTS {name}")
        admin.execute(f"CREATE DATABASE {name}")

    with psycopg.connect(dbname=name, autocommit=True, **settings) as db:
        db.execute(Path("postgres/init.sql").read_text())

    yield name
