import service
from base_db_engine import get_session, async_session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn import run as uvicorn_run
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import requests
from starlette.responses import Response
from datetime import timedelta, date
# from werkzeug.security import generate_password_hash, check_password_hash

app = FastAPI()

SECRET_KEY = "mysecretkey"  # подложить енв переменную
login_manager = LoginManager(SECRET_KEY, token_url="/login", use_cookie=True)

@login_manager.user_loader()
async def load_user(user):
    async with async_session() as session:
        cur_user = await service.get_pass(user, session)
        return cur_user.username

STAFF_BASE_URL = "http://staff:5555"
CALENDAR_BASE_URL = "http://calendar:5557"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://158.160.53.9:3000", "http://158.160.53.9", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    username: str
    email: str
    phone_number: str
    telegram: str
    user_about: str
    position: str
    photo_url: str
    meta: str
    manager_username: int
    name_of_unit: str
    date_of_birth: str
    start_date: str


@app.post("/login")
async def login(data: dict, response: Response, session: AsyncSession = Depends(get_session)):
    username = data.get("username")
    password = data.get("password")
    user = await service.get_pass(username, session)
    if user is None or user.password != password:
        raise InvalidCredentialsException
    response = Response("OK", status_code=200, headers=None, media_type=None)
    access_token = login_manager.create_access_token(data=dict(sub=username), expires=timedelta(hours=12))
    login_manager.set_cookie(response, access_token)
    return response


@app.post("/register")
async def register_user(data: dict, username=Depends(login_manager), session: AsyncSession = Depends(get_session)):
    user = await service.get_pass(username, session)
    if user is None or not user.is_admin:
        raise InvalidCredentialsException
    service.create_user(data.get("username"), data.get("password"), data.get("is_admin"), session)
    data_req = UserCreateSchema.parse_obj(data)
    response = requests.post(f'{STAFF_BASE_URL}/user', json=data_req.model_dump())
    if response.status_code == 200:
        response = requests.put(f'{CALENDAR_BASE_URL}/calendar/{data.get("username")}/url', json=data_req.model_dump())
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.reason)
    else:
        raise HTTPException(status_code=response.status_code, detail=response.reason)
    
    

@app.put("/change_password/{username}")
async def change_user_password(username: str, data: dict, current_user=Depends(login_manager)):
    new_password = data.get("new_password")
    if not current_user.is_admin and current_user.username != username:
        raise HTTPException(status_code=403, detail="You are not authorized to change this user's password")
    
    # password_hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16)
    res = await service.set_pass(username, new_password)
    if res:
        return {"message": "Password changed successfully"}
    else:
        HTTPException(status_code=500, detail="Try again later")

# region: staff service
@app.get("/user/{username}")
async def get_user(username: str, current_user=Depends(login_manager)):
    if current_user is None: 
        raise InvalidCredentialsException
    response = requests.get(f'{STAFF_BASE_URL}/user/{username}')
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.reason)


@app.get("/users/{request}")
async def search_users(request: str, current_user=Depends(login_manager)):
    response = requests.get(f'{STAFF_BASE_URL}/users/{request}')
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.reason)


@app.put("/user/{username}")
async def update_user(username: str, data: dict, current_user=Depends(login_manager)):
    if not current_user.is_admin and current_user.username != username:
        raise HTTPException(status_code=403, detail="You are not authorized to change this user's info")
    data_req = UserCreateSchema.parse_obj(data)
    response = requests.put(f'{STAFF_BASE_URL}/user/{username}', json=data_req)
    if current_user.is_admin:
        response = requests.put(f'{STAFF_BASE_URL}/user/{username}/admin', json=data_req) 
        
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.reason)
# endregion
# region: calendar
@app.get("/calendar/{username}")
async def get_user(username: str, count: int, current_user=Depends(login_manager)):
    if current_user is None: 
        raise InvalidCredentialsException
    response = requests.get(f'{CALENDAR_BASE_URL}/calendar/{username}?count=' + str(count))
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.reason)
    

@app.post("/calendar/{username}/url")
async def get_user(username: str, data: dict, current_user=Depends(login_manager)):
    if current_user is None: 
        raise InvalidCredentialsException
    response = requests.post(f'{CALENDAR_BASE_URL}/calendar/{username}', json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.reason)
# endregion

# TODO это сервис по типу gateway, то есть каждая новая ручка в новом сервисе дублируется здесь и на нее идет запрос

if __name__ == "__main__":
    # init_models()
    uvicorn_run(app, host="0.0.0.0", port=5556)
