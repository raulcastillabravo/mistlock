from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    quantity_sold = Column(Integer, nullable=False, default=0)
    revenue = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)
