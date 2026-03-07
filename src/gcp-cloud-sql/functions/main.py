import os, io, csv
from google.cloud import storage
from firebase_functions import storage_fn
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, Session

DATABASE_URL = os.environ["DATABASE_URL"]
STORAGE_BUCKET = os.environ["STORAGE_BUCKET"]

Base = declarative_base()
engine = create_engine(DATABASE_URL)
storage_client = storage.Client()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Initialize database schema
Base.metadata.create_all(engine)

@storage_fn.on_object_finalized(bucket=STORAGE_BUCKET)
def process_csv(event: storage_fn.CloudEvent):
    bucket = storage_client.bucket(event.data.bucket)
    blob = bucket.blob(event.data.name)
    data = blob.download_as_text()
    
    with Session(engine) as session:
        reader = csv.DictReader(io.StringIO(data))
        session.add_all([User(name=row['name'], email=row['email']) for row in reader])
        session.commit()
    
    print(f"✓ Processed file: {event.data.name}")
