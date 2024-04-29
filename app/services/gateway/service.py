from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Auth


async def get_pass(username: str, session: AsyncSession):
    result = await session.execute(select(Auth).where(Auth.username == username))
    res_scal = result.scalars().all()
    if (len(res_scal) == 0):
        return None
    return res_scal[0]

async def set_pass(username: str, password: str, session: AsyncSession):
    user = await session.query(Auth).filter(Auth.username == username).first()
    if user:
        user.password = password
        await session.commit()
        return True
    return False

async def create_user(username: str, password: str, is_admin: bool, session: AsyncSession):
    new_record = Auth(username=username, password=password, is_admin=is_admin)
    session.add(new_record)
    await session.commit()
