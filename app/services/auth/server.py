import service
from base_db_engine import get_session, init_models
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uvicorn import run as uvicorn_run
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

app = FastAPI()

SECRET_KEY = "mysecretkey"  # подложить енв переменную
login_manager = LoginManager(SECRET_KEY, token_url="/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    id: str
    password: str


@app.post("/login")
async def get_user(data: User, session: AsyncSession = Depends(get_session)):
    user = await service.get_pass(data.id)
    if user is None or user.password != data.password:
        raise InvalidCredentialsException

    access_token = login_manager.create_access_token(data.dict())
    return {"access_token": access_token}


@app.get("/verify-token")
async def verify_token(token: str = Depends(login_manager)):
    return {"message": "Token is valid"}


if __name__ == "__main__":
    init_models()
    uvicorn_run(app, host="0.0.0.0", port=5556)
