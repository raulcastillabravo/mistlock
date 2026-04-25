from datetime import datetime, UTC
from mongoengine import Document, StringField, EmailField, DateTimeField


class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.now(UTC))

    meta = {
        "collection": "users",
        "indexes": ["email"],
    }
