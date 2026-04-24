import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()


def connect_to_mongo():
    """Establish connection to MongoDB"""
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    db = os.getenv("MONGO_DB")

    connection_string: str = (
        f"mongodb://{user}:{password}@{host}:{port}/{db}?authSource=admin"
    )

    connect(db=db, host=connection_string, alias="default", uuidRepresentation='standard')
