import os, io, csv
from firebase_admin import initialize_app, storage
from firebase_functions import storage_fn
from sqlalchemy import create_all, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, Session

initialize_app()
Base = declarative_base()
engine = create_engine(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mve_db"))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

@storage_fn.on_object_finalized()
def process_csv(event: storage_fn.CloudEvent):
    bucket = storage.bucket(event.data.bucket)
    blob = bucket.blob(event.data.name)
    data = blob.download_as_text()
    
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        reader = csv.DictReader(io.StringIO(data))
        session.add_all([User(name=row['name'], email=row['email']) for row in reader])
        session.commit()
    print(f"Processed {event.data.name}")
