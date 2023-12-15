from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User


async def get_user(user_id: int, session: AsyncSession):
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalars().one()


async def get_users(request: str, session: AsyncSession):
    result = await session.execute(
        select(User).where(
            (User.nickname.ilike(f"%{request}%"))
            | (User.first_name.ilike(f"%{request}%"))
            | (User.last_name.ilike(f"%{request}%"))
            | (User.position.ilike(f"%{request}%"))
        )
    )
    return result.scalars().all()
