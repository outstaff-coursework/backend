from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import Calendar


async def get_calendar_url(username: str, session: AsyncSession):
    result = await session.execute(select(Calendar).where(Calendar.username == username))
    res_scal = result.scalars().all()
    if (len(res_scal) == 0):
        return None
    return res_scal[0]

async def create_calendar(username: str, calendar_url: str, session: AsyncSession):
    new_record = Calendar(username=username, calendar_url=calendar_url)
    session.add(new_record)
    await session.commit()
    return True 