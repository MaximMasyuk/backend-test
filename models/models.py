from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from models.db_connection import engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "userdb"
    id = Column(Integer, CheckConstraint('id >= 0'), primary_key=True)
    username = Column(String, unique=True, index=True)
    surname = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    eth_address = Column(String)
    signature = Column(String)
    password_hash = Column(String)

Base.metadata.create_all(bind=engine)