from dotenv import load_dotenv

from src.models.user import User
from src.models.utils import create_tables, get_session

load_dotenv()


def insert_sample_data():
    with get_session() as session:
        users = [
            User(name="John Doe", email="john@example.com"),
            User(name="Jane Smith", email="jane@example.com"),
            User(name="Bob Johnson", email="bob@example.com")
        ]

        emails = [user.email for user in users]
        existing = {
            email for (email,) in session.query(User.email)
            .filter(User.email.in_(emails))
        }
        new_users = [user for user in users if user.email not in existing]

        session.add_all(new_users)
        session.commit()

        already = session.query(User).filter(User.email.in_(existing)).all()

        print("\nInserted users:")
        for user in new_users:
            print(f"  - {user}")

        print("\nAlready inserted users:")
        for user in already:
            print(f"  - {user}")


if __name__ == "__main__":
    create_tables()

    print("\nInserting sample data...")
    insert_sample_data()

    print("\n✓ Done! You can now connect with DBeaver to see the data.")
