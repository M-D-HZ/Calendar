from fastapi import APIRouter
from wrapper import find_user, get_users
from pydantic import BaseModel

userRouter = APIRouter()

@userRouter.get("/{u_id}")
def get_user(u_id: int):
    response = find_user(u_id)
    return response

@userRouter.get("")
def get_all_users():
    response = get_users()
    return response


