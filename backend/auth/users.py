from fastapi import APIRouter, HTTPException
from wrapper import find_user, get_users
from pydantic import BaseModel

userRouter = APIRouter()

@userRouter.get("/{username}")
def get_user(username: str):
    try:
        response = find_user(username)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@userRouter.get("")
def get_all_users():
    try:
        response = get_users()
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


