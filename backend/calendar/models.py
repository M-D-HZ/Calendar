from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base model which our classes will inherit from"""
    
class ShareCalendar(Base):
    __tablename__ = "calendar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user1 = Column(String)
    user2 = Column(String)