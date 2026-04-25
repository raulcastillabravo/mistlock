import os
import pytest
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from src.models.user import User

load_dotenv(".env.test", override=True)


@pytest.fixture(scope="module", autouse=True)
def db_connection():
    connect(host=os.getenv("MONGO_URI"))
    yield


def test_user():
    User.objects.delete()
    assert User.objects.count() == 0

    # Create
    user = User(name="Test User", email="test@example.com")
    user.save()
    assert User.objects.count() == 1
    
    # Read
    found_user = User.objects(email="test@example.com").first()
    assert found_user is not None
    assert found_user.name == "Test User"

    # Update
    found_user.name = "Updated User"
    found_user.save()
    
    updated_user = User.objects(email="test@example.com").first()
    assert updated_user.name == "Updated User"

    # Delete
    updated_user.delete()
    assert User.objects.count() == 0
