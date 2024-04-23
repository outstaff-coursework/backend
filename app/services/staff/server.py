from typing import List

import service
from base_db_engine import get_session, init_models
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn import run as uvicorn_run
import asyncio
from models import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    photo_url: str
    meta: str
    manager_id: str
    name_of_unit: str

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    nickname: str
    email: str
    phone_number: str
    telegram: str
    user_about: str
    position: str
    photo_url: str
    meta: str
    manager_id: int
    name_of_unit: str

@app.get("/user/{user_id}", response_model=UserInfoSchema)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await service.get_user(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInfoSchema(
        name=user.first_name + " " + user.last_name + " " + user.patronymic,
        nickname=user.nickname,
        email=user.email,
        telegram=user.telegram,
        phone_number=user.phone_number,
        user_about=user.user_about,
        position=user.position,
        photo_url=user.photo_url,
        meta = user.meta,
        manager_id = user.manager_id,
        name_of_unit = user.name_of_unit,
    )


@app.get("/users/{request}", response_model=UserSearchList)
async def search_users(request: str, session: AsyncSession = Depends(get_session)):
    users = await service.get_users(request, session)
    items = [
        UserSearchSchema(
            name=user.first_name + " " + user.last_name + " " + user.patronymic,
            user_id=user.user_id,
            position=user.position,
        )
        for user in users
    ]
    return UserSearchList(items=items)

@app.put("/user")
async def create_user(userSchema: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = User(
        nickname = userSchema.nickname,
        first_name = userSchema.first_name,
        last_name = userSchema.last_name,
        patronymic = userSchema.patronymic,
        email = userSchema.email,
        phone_number = userSchema.phone_number,
        telegram = userSchema.telegram,
        user_about = userSchema.user_about,
        position = userSchema.position,
        meta = userSchema.meta,
        manager_id = userSchema.manager_id,
        name_of_unit = userSchema.name_of_unit,
        photo_url = userSchema.photo_url,
        )
    result = await service.create_user(user, session)
    if result:
        return {"200":"OK"}
    else:
        raise HTTPException(status_code=400, detail="Cant create user")

@app.post("/user/{user_id}")
async def create_user(user_id: int, userSchema: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = User(
        nickname = userSchema.nickname,
        first_name = userSchema.first_name,
        last_name = userSchema.last_name,
        patronymic = userSchema.patronymic,
        email = userSchema.email,
        phone_number = userSchema.phone_number,
        telegram = userSchema.telegram,
        user_about = userSchema.user_about,
        position = userSchema.position,
        meta = userSchema.meta,
        manager_id = userSchema.manager_id,
        name_of_unit = userSchema.name_of_unit,
        photo_url = userSchema.photo_url,
        )
    result = await service.update_user(user_id, user, session)
    if result:
        return {"200":"OK"}
    else:
        raise HTTPException(status_code=400, detail="Cant create user")

if __name__ == "__main__":
    # asyncio.run(init_models())
    uvicorn_run(app, host="0.0.0.0", port=5555)
