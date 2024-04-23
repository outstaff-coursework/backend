from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User


async def get_user(user_id: int, session: AsyncSession):
    result = await session.execute(select(User).where(User.user_id == user_id))
    res_scal = result.scalars().all()
    if (len(res_scal) == 0):
        return None
    return res_scal[0]


async def get_users(request: str, session: AsyncSession):
    result = await session.execute(
        select(User).where(
            (User.nickname.ilike(f"%{request}%")) |
            (User.first_name.ilike(f"%{request}%")) |
            (User.last_name.ilike(f"%{request}%")) |
            (User.position.ilike(f"%{request}%"))
        )
    )
    return result.scalars().all()

async def create_user(user_data: User, session: AsyncSession):
    try:
        session.add(user_data)
        await session.commit()

        await session.refresh(user_data)
    except:
        return False
    return True


async def update_user(user_id: int, user_data: User, session: AsyncSession):
    result = await session.execute(update(User).where(User.user_id == user_id).values(user_data))
    if result.rowcount == 0:
        return False
    return True
