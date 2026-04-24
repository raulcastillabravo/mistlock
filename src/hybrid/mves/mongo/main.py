from src.models.user import User
from src.utils.utils import connect_to_mongo


def run_example():
    """Run MongoDB CRUD example"""
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    connect_to_mongo()
    print("✓ Connected successfully")

    # Create a user
    print("\nCreating a user...")
    user = User(name="John Doe", email="john.doe@example.com")
    user.save()
    print(f"✓ User created: {user}")

    # Read the user
    print("\nReading users from database...")
    users = User.objects.all()
    for u in users:
        print(f"  - {u}")

    print("\n✓ Done! You can now connect with MongoDB Compass to see the data.")


if __name__ == "__main__":
    try:
        run_example()
    except Exception as e:
        print(f"✗ Error: {e}")