from fastapi import FastAPI, HTTPException
from icalendar import Calendar
import requests
from base_db_engine import get_session
from uvicorn import run as uvicorn_run
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import service
from datetime import datetime
from typing import List

app = FastAPI()

class Event(BaseModel):
    summary: str
    description: str
    participants: List[str]
    end_time: datetime
    start_time: datetime

class Events(BaseModel):
    events: List[Event]

@app.get("/calendar/{username}")
async def get_calendar(username: str, session: AsyncSession = Depends(get_session)):
    calendar = await service.get_calendar_url(username, session)
    if calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    cal = Calendar.from_ical(requests.get(calendar.calendar_url).text)
    events = [
        Event(
            summary=str(component.get('summary', b'')),
            description=str(component.get('description', b'')),
            participants=[str(attendee) for attendee in component.get('attendees', [])],
            end_time=component.get('dtend').dt,
            start_time=component.get('dtstart').dt
        )
        for component in cal.walk() if component.name == "VEVENT"
    ]
    return events

@app.put("/calendar/{username}/url")
async def put_calendar(username: str, data: dict, session: AsyncSession = Depends(get_session)):
    url = data.get("calendar_url")
    if service.create_calendar(username, url, session):
        return {200:"OK"}

if __name__ == "__main__":
    # init_models()
    uvicorn_run(app, host="0.0.0.0", port=5557)