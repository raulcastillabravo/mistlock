import os
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("SQL_CONNECTION_STRING")

# SQLAlchemy requires a specific prefix
params = quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

Base = declarative_base()

class User(Base):
    """User model for UserDB."""
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False, unique=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

# Database access session
SessionLocal = sessionmaker(bind=engine)

def save_user(name, email):
    """Save a user record to the database.
    
    Args:
        name: User's name
        email: User's email
    """
    session = SessionLocal()
    try:
        new_user = User(Name=name, Email=email)
        session.add(new_user)
        session.commit()
    finally:
        session.close()
