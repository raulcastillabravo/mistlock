from src.models.user import User
from src.models.utils import get_session


def insert_sample_data():
    session = get_session()

    try:
        users = [
            User(name="John Doe", email="john@example.com"),
            User(name="Jane Smith", email="jane@example.com"),
            User(name="Bob Johnson", email="bob@example.com")
        ]

        session.add_all(users)
        session.commit()
        print(f"✓ Inserted {len(users)} users successfully")

        # Query and display inserted data
        all_users = session.query(User).all()
        print("\nInserted users:")
        for user in all_users:
            print(f"  - {user}")

    except Exception as e:
        session.rollback()
        print(f"✗ Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("\nInserting sample data...")
    insert_sample_data()

    print("\n✓ Done! You can now connect with DBeaver to see the data.")
