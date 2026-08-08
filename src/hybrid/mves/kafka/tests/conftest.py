import os

import pytest
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.test", override=True)


@pytest.fixture
def topic() -> str:
    """Creates a dedicated topic per test and removes it afterwards."""
    admin = AdminClient(
        {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}
    )
    name = os.getenv("KAFKA_TOPIC")

    for future in admin.create_topics([NewTopic(name, 1, 1)]).values():
        future.result()

    yield name

    for future in admin.delete_topics([name]).values():
        future.result()
