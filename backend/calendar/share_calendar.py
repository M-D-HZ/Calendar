from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wrapper import calendar_sharing, get_all_calendars, get_shares

calendarRouter = APIRouter()

class shareCalendarRequest(BaseModel):
    owner: str
    receiver: str

@calendarRouter.post("")
def share_calendar(sharedCalendarRequest: shareCalendarRequest):
    try:
        response = calendar_sharing(sharedCalendarRequest.owner, sharedCalendarRequest.receiver)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@calendarRouter.get("")
def all_calendars():
    try:
        response = get_all_calendars()
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@calendarRouter.get("/{user}")
def shares(user: str):
    try:
        response = get_shares(user)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))