from fastapi import APIRouter
from wrapper import create_user, user_login
from pydantic import BaseModel

authrouter = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

@authrouter.post("/register")
def register_user(registerRequest: RegisterRequest):
    response = create_user(registerRequest.username, registerRequest.password)
    return response

class LoginRequest(BaseModel):
    username: str
    password: str

@authrouter.post("/login")
def login_user(logingRequest: LoginRequest):
    response = user_login(logingRequest.username, logingRequest.password)
    return response



