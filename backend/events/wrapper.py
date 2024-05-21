import os

from models import eventModel
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker


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


def add_event(title: str, description: str, date: str, public: bool, organizer: str):
    try:
        if (
            session.query(eventModel)
            .filter(
                eventModel.title == title
                and eventModel.date == date
                and eventModel.organizer == organizer
                and eventModel.public == public
                and eventModel.description == description
            )
            .first()
        ):
            raise Exception("Event already exists")
        event = eventModel(
            title=title,
            description=description,
            date=date,
            public=public,
            organizer=organizer,
        )
        session.add(event)
        session.commit()
        return {
            "message": "Event created successfully",
            "Event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "public": event.public,
                "organizer": event.organizer,
            },
        }
    except Exception as e:
        session.rollback()
        raise Exception(e) from e


def get_all_events():
    try:
        events = session.query(eventModel).all()
        return {
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "date": event.date,
                    "public": event.public,
                    "organizer": event.organizer,
                }
                for event in events
            ]
        }
    except Exception as e:
        raise Exception(e) from e


def find_event(event_id: int):
    try:
        event = session.query(eventModel).filter(eventModel.id == event_id).first()
        if event:
            return {
                "event": {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "date": event.date,
                    "public": event.public,
                    "organizer": event.organizer,
                }
            }
        raise Exception("Event not found")
    except Exception as e:
        raise Exception(e) from e
