from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base model which our classes will inherit from"""
    
class eventModel(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    date = Column(Date)
    public = Column(Boolean)
    organizer = Column(String)