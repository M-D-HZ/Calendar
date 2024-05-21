from fastapi import FastAPI
from share_calendar import calendarRouter

app = FastAPI()

app.include_router(calendarRouter, prefix="/calendar", tags=["calendar"])

