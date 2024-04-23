import service
from base_db_engine import get_session, init_models
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn import run as uvicorn_run
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from werkzeug.security import generate_password_hash, check_password_hash

app = FastAPI()

SECRET_KEY = "mysecretkey"  # подложить енв переменную
login_manager = LoginManager(SECRET_KEY, token_url="/login")

STAFF_BASE_URL = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    password: str
    is_admin: bool


@app.post("/login")
async def get_user(data: dict, session: AsyncSession = Depends(get_session)):
    username = data.get("username")
    password = data.get("password")
    user = await service.get_pass(username, session)
    if user is None or user.password_hash != password:
        raise InvalidCredentialsException

    access_token = login_manager.create_access_token(data=dict(sub=username))
    return {"access_token": access_token}


@app.post("/register")
async def register_user(data: dict, username=Depends(login_manager), session: AsyncSession = Depends(get_session)):
    user = await service.get_pass(username)
    if user is None or not user.is_admin:
        raise InvalidCredentialsException
    
    # TODO допилить метод, сделать регистрацию тут + в сервисе стаффа
    
@app.put("/change_password/{username}")
async def change_user_password(username: str, data: dict, current_user=Depends(login_manager)):
    new_password = data.get("new_password")
    if not current_user.is_admin and current_user.username != username:
        raise HTTPException(status_code=403, detail="You are not authorized to change this user's password")
    
    password_hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16)
    res = await service.set_pass(username, password_hash)
    if res:
        return {"message": "Password changed successfully"}
    else:
        HTTPException(status_code=500, detail="Try again later")


# TODO это сервис по типу gateway, то есть каждая новая ручка в новом сервисе дублируется здесь и на нее идет запрос

if __name__ == "__main__":
    # init_models()
    uvicorn_run(app, host="0.0.0.0", port=5556)
