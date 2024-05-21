from fastapi import FastAPI
from event import eventsRouter

app = FastAPI()

app.include_router(eventsRouter, prefix="/events", tags=["events"])
