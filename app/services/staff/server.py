from fastapi import FastAPI
from fastapi import Depends
import service
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn import run as uvicorn_run
import base_db_engine
from pydantic import BaseModel
from typing import List
from base_db_engine import get_session, init_models

app = FastAPI()

class UserSearchSchema(BaseModel):
    name: str
    user_id: int
    position: str

class UserSearchList(BaseModel):
    items: List[UserSearchSchema]

class UserInfoSchema(BaseModel):
    name: str
    nickname: str
    email: str
    telegram: str
    phone_number: str
    user_about: str
    position: str

@app.get("/user/{user_id}", response_model=UserInfoSchema)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await service.get_user(user_id, session)
    return UserInfoSchema(name=user.first_name + " " + user.last_name + " " + user.patronymic, nickname=user.nickname,
                          email=user.email, telegram=user.telegram, phone_number=user.phone_number, user_about=user.user_about,
                          position=user.position)

@app.get("/users/{request}", response_model=UserSearchList)
async def search_users(request: str, session: AsyncSession = Depends(get_session)):
    users = await service.get_users(request, session)
    items = [UserSearchSchema(name=user.first_name + " " + user.last_name + " " + user.patronymic,
                              user_id=user.user_id, position=user.position) for user in users]
    return UserSearchList(items=items)

if __name__ == "__main__":
    init_models()
    uvicorn_run(app, host="0.0.0.0", port=5555)
        