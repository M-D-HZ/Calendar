import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import engagementModel


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

def add_engagement(user: str, event_id: int, invite_status: str = 'pending'):
    try:
        engagement = session.query(engagementModel).filter_by(user=user, event_id=event_id).first()
        if engagement:
            raise Exception("User is already invited to this event")
        engagement = engagementModel(user=user, event_id=event_id, invite_status=invite_status)
        session.add(engagement)
        session.commit()
        return "Engagement added successfully"
    except Exception as e:
        session.rollback()
        raise Exception(str(e))

def get_all_engagements():
    try:
        engagements = session.query(engagementModel).all()
        return [{
            "id": engagement.id,
            "user": engagement.user,
            "event_id": engagement.event_id,
            "invite_status": engagement.invite_status
            } for engagement in engagements]
    except Exception as e:
        raise Exception(str(e))
    
def find_user_engagements(user: str):
    try:
        engagements = session.query(engagementModel).filter_by(user=user).all()
        return [{
            "id": engagement.id,
            "user": engagement.user,
            "event_id": engagement.event_id,
            "invite_status": engagement.invite_status
            } for engagement in engagements]
    except Exception as e:
        raise Exception(str(e))

def update_engagement_status(user: str, event_id: int, invite_status: str):
    try:
        engagement = session.query(engagementModel).filter_by(user=user, event_id=event_id).first()
        if not engagement:
            raise Exception("Engagement not found")
        engagement.invite_status = invite_status
        session.commit()
        return "Engagement updated successfully"
    except Exception as e:
        session.rollback()
        raise Exception(str(e))