import os
import json
import boto3
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db_config():
    """Fetch credentials from AWS Secrets Manager."""
    # LocalStack provides LOCALSTACK_HOSTNAME inside the Lambda container
    if ls_host := os.getenv("LOCALSTACK_HOSTNAME"):
        endpoint = f"http://{ls_host}:4566"
    else:
        endpoint = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    
    client = boto3.session.Session().client(
        service_name='secretsmanager',
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        endpoint_url=endpoint
    )
    response = client.get_secret_value(SecretId='postgres-credentials')
    return json.loads(response['SecretString'])

def get_session():
    """Create SQLAlchemy session using secrets."""
    config = get_db_config()
    uri = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
    engine = create_engine(uri)
    return sessionmaker(bind=engine)()
