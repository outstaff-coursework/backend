from fastapi import FastAPI, HTTPException
from icalendar import Calendar
import requests
from base_db_engine import get_session
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
    url = await service.get_calendar_url(username, session)
    cal = Calendar(requests.get(url).text)
    events = [
        Event(
            summary=str(component.get('summary', b'').decode('utf-8')),
            description=str(component.get('description', b'').decode('utf-8')),
            participants=[str(attendee).split(':')[1] for attendee in component.get('attendee', [])],
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
