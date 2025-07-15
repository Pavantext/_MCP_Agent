from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    outlook_access_token = Column(String, nullable=True)
    outlook_refresh_token = Column(String, nullable=True)
    github_access_token = Column(String, nullable=True)
    teams_access_token = Column(String, nullable=True)
    teams_refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow) 