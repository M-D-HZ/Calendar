from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import ShareCalendar
import os

def get_env_variable(name: str):
    return os.getenv(name, "")

def get_url():
    return URL.create(
        drivername="postgresql+psycopg2",
        username=get_env_variable("POSTGRES_USER"),
        password=get_env_variable("POSTGRES_PASSWORD"),
        host=get_env_variable("POSTGRES_HOST"),
        port=5432, 
        database=get_env_variable("POSTGRES_DB"),
    )

sqlengine = create_engine(get_url(), echo=True)

Session = sessionmaker(bind=sqlengine)
session = Session()

def calendar_sharing(user1: str, user2: str):
    try:
        shared = session.query(ShareCalendar).filter(ShareCalendar.user1 == user1, ShareCalendar.user2 == user2).first()
        if shared:
            raise Exception("Calendar already shared")
        session.add(ShareCalendar(user1=user1, user2=user2))
        session.commit()
        return {"message": "Calendar shared"}
    except Exception as e:
        session.rollback()
        raise Exception(str(e))
    
def get_all_calendars():
    try:
        calendars = session.query(ShareCalendar).all()
        return [{"id": calendar.id, "user1": calendar.user1, "user2": calendar.user2} for calendar in calendars]
    except Exception as e:
        raise Exception(str(e))

def get_shares(user: str):
    try:
        calendars = session.query(ShareCalendar).filter(ShareCalendar.user2 == user).all()
        return [{"id": calendar.id, "user1": calendar.user1, "user2": calendar.user2} for calendar in calendars]
    except Exception as e:
        raise Exception(str(e))