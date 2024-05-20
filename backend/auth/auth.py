from fastapi import APIRouter
from wrapper import create_user
from pydantic import BaseModel

authrouter = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

@authrouter.post("/register")
def register_user(registerRequest: RegisterRequest):
    response = create_user(registerRequest.username, registerRequest.password)
    return response