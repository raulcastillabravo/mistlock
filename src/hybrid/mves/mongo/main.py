import os
from dotenv import load_dotenv
from mongoengine import connect
from src.models.user import User

load_dotenv()

connect(host=os.getenv("MONGO_URI"))


def run_example():
    email = "john.doe@example.com"
    user = User.objects(email=email).first()

    if user:
        print(f"✓ User found: {user.name} ({user.email})")
    else:
        user = User(name="John Doe", email=email)
        user.save()
        print(f"✓ User created: {user.name} ({user.email})")


if __name__ == "__main__":
    run_example()