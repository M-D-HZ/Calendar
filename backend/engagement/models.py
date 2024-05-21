from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base model which our classes will inherit from"""
    
class engagementModel(Base):
    __tablename__ = 'engagement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String)
    event_id = Column(Integer)
    invite_status = Column(String)