from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    user = os.getenv('METABASE_USER')
    password = os.getenv('METABASE_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    db = os.getenv('METABASE_DB')

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(connection_string, echo=True)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
