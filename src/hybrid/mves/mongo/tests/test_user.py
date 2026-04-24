import pytest
from src.models.user import User
from src.utils.utils import connect_to_mongo


@pytest.fixture(scope="module", autouse=True)
def db_connection():
    connect_to_mongo()
    # Clear collection before tests
    User.objects.delete()
    yield
    # Clear collection after tests
    User.objects.delete()


def test_user_crud():
    # 1. Query and find no documents
    assert User.objects.count() == 0

    # 2. Write a document and read it
    user = User(name="Test User", email="test@example.com")
    user.save()
    assert User.objects.count() == 1
    
    found_user = User.objects(email="test@example.com").first()
    assert found_user is not None
    assert found_user.name == "Test User"

    # 3. Update the document
    found_user.name = "Updated User"
    found_user.save()
    
    updated_user = User.objects(email="test@example.com").first()
    assert updated_user.name == "Updated User"

    # 4. Delete the document
    updated_user.delete()
    assert User.objects.count() == 0
