from fastapi import APIRouter, HTTPException
from wrapper import create_user, user_login
from pydantic import BaseModel

authrouter = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

@authrouter.post("/register")
def register_user(registerRequest: RegisterRequest):
    try:
        response = create_user(registerRequest.username, registerRequest.password)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

class LoginRequest(BaseModel):
    username: str
    password: str

@authrouter.post("/login")
def login_user(logingRequest: LoginRequest):
    try:
        response = user_login(logingRequest.username, logingRequest.password)
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
