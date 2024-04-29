from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Auth


async def get_pass(user_id: int, session: AsyncSession):
    result = await session.execute(select(Auth).where(Auth.user_id == user_id))
    res_scal = result.scalars().all()
    if (len(res_scal) == 0):
        return None
    return res_scal[0]
