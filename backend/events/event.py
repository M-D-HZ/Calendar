from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from wrapper import add_event, get_all_events, find_event

eventsRouter = APIRouter()

class EventRequest(BaseModel):
    title: str
    description: str = None
    date: date
    public: bool = True
    organizer: str = None

@eventsRouter.post("/create")
def create_event(event: EventRequest):
    try:
        response = add_event(event.title, event.description, event.date, event.public, event.organizer)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@eventsRouter.get("")
def get_events():
    try:
        response = get_all_events()
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@eventsRouter.get("/{event_id}")
def get_event(event_id: int):
    try:
        response = find_event(event_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
