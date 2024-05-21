from fastapi import APIRouter
from wrapper import get_user, get_all_users
from pydantic import BaseModel

userRouter = APIRouter()

@userRouter.get("/{u_id}")
def get_user(u_id: int):
    response = get_user(u_id)
    return response

@userRouter.get("/all")
def get_all_users():
    response = get_all_users()
    return response


