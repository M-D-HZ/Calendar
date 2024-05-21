from fastapi import FastAPI
from engage import engageRouter

app = FastAPI()

app.include_router(engageRouter, prefix="/engagement", tags=["engagement"])