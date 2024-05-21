from fastapi import FastAPI
from auth import authrouter
from users import userRouter

app = FastAPI()
    
app.include_router(authrouter, prefix="/auth", tags=["auth"])
app.include_router(userRouter, prefix="/users", tags=["users"])
