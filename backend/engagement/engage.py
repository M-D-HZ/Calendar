from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from wrapper import add_engagement, get_all_engagements, find_user_engagements, update_engagement_status

engageRouter = APIRouter()

class EngageRequest(BaseModel):
    user: str
    event_id: int
    invite_status: str = None

@engageRouter.post("")
def invite_user(engage: EngageRequest):
    try:
        response = add_engagement(engage.user, engage.event_id, engage.invite_status)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@engageRouter.get("")
def get_engagements():
    try:
        response = get_all_engagements()
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@engageRouter.get("/{user}")
def get_user_engagements(user: str):
    try:
        response = find_user_engagements(user)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@engageRouter.put("")
def update_engagement(engage: EngageRequest):
    try:
        response = update_engagement_status(engage.user, engage.event_id, engage.invite_status)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

