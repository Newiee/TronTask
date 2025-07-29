
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String)
    time_of_request = Column(TIMESTAMP(timezone=False))
