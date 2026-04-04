from mongoengine import Document, StringField, EmailField, DateTimeField, connect
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['email']
    }
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

def get_connection():
    """Establish connection to MongoDB"""
    user = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASSWORD')
    host = os.getenv('MONGO_HOST')
    port = os.getenv('MONGO_PORT')
    db = os.getenv('MONGO_DB')
    
    connection_string = f"mongodb://{user}:{password}@{host}:{port}/{db}?authSource=admin"
    
    return connect(
        db=db,
        host=connection_string,
        alias='default'
    )