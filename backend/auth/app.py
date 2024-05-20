from fastapi import FastAPI, APIRouter
from auth import authrouter

app = FastAPI()
    
app.include_router(authrouter)