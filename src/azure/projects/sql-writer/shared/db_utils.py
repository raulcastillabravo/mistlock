import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def get_session():
    """Returns a new database session instance."""
    connection_string = os.getenv("SQL_CONNECTION_STRING")

    params = quote_plus(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    session = sessionmaker(bind=engine)

    return session()
