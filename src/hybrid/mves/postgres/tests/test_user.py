from dotenv import load_dotenv

from src.models.user import User
from src.models.utils import get_session

load_dotenv(".env.test", override=True)


def test_user():
    with get_session() as session:
        session.query(User).delete()
        session.commit()
        assert session.query(User).count() == 0

        # Create
        session.add(User(name="Test User", email="test@example.com"))
        session.commit()
        assert session.query(User).count() == 1

        # Read
        found = session.query(User).filter_by(email="test@example.com").first()
        assert found is not None
        assert found.name == "Test User"

        # Update
        found.name = "Updated User"
        session.commit()
        updated = session.query(User).filter_by(email="test@example.com").first()
        assert updated.name == "Updated User"

        # Delete
        session.delete(updated)
        session.commit()
        assert session.query(User).count() == 0
