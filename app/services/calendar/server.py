from fastapi import FastAPI, HTTPException
from icalendar import Calendar
import requests
from base_db_engine import get_session
from uvicorn import run as uvicorn_run
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import service
import pytz
from datetime import datetime, timedelta, date, time
from typing import List, Optional

app = FastAPI()

class Event(BaseModel):
    summary: str
    description: str
    participants: List[str]
    end_time: time
    start_time: time
    start_date: date
    end_date: date

class Events(BaseModel):
    events: List[Event]
    current_event: Optional[Event]
    dates: List[date]

@app.get("/calendar/{username}")
async def get_calendar(username: str, count: int, session: AsyncSession = Depends(get_session)):
    calendar = await service.get_calendar_url(username, session)
    if calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    cal = Calendar.from_ical(requests.get(calendar.calendar_url).text)
    start_date = datetime(2021, 3, 17, 9, 0, 0)
    end_date = datetime(2021, 3, 17, 9, 0, 0)
    # tz=pytz.timezone("Etc/GMT-7")
    if count == 3:
        start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=3)
    elif count == 7:
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7)
    start_date = start_date.replace(tzinfo=pytz.UTC)
    end_date = end_date.replace(tzinfo=pytz.UTC)
    events = []
    dates = []
    print(type(start_date))
    print(type(end_date))
    for single_date in (start_date.date() + timedelta(n) for n in range(count)):
        dates.append(single_date)
    current_event = None
    for component in cal.walk():
        if component.name == "VEVENT":
            print(component.get('DTSTART').dt.replace(tzinfo=pytz.UTC))
            event_start = component.get('DTSTART').dt.replace(tzinfo=pytz.UTC)
            event_end = component.get('DTEND').dt.replace(tzinfo=pytz.UTC)
            if event_start >= start_date and event_end < end_date:
                participants = component.get('ATTENDEE', [])
                print(participants)
                participants_list = []
                if type(participants) != list:
                    participants_list = [participants]
                else:
                    participants_list = [p for p in participants]
                event_title = str(component.get('SUMMARY'))
                event_description = str(component.get('DESCRIPTION'))
                event = Event(
                    summary=event_title,
                    description=event_description,
                    participants=participants_list,
                    start_time=(event_start + timedelta( hours=3 )).time(),
                    start_date=event_start.date(), 
                    end_time=(event_end + timedelta( hours=3 )).time(),
                    end_date=event_end.date(),
                )
                events.append(event)
                if event_start <= datetime.now(pytz.UTC) <= event_end:
                    current_event = event
        
    return Events(events=events, current_event=current_event, dates=dates)

@app.put("/calendar/{username}/url")
async def put_calendar(username: str, data: dict, session: AsyncSession = Depends(get_session)):
    url = data.get("calendar_url")
    if service.create_calendar(username, url, session):
        return {200:"OK"}

if __name__ == "__main__":
    # init_models()
    uvicorn_run(app, host="0.0.0.0", port=5557)