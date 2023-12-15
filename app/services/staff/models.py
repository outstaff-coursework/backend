from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from base_db_engine import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    telegram = Column(String, unique=True, nullable=True)
    user_about = Column(String, nullable=True)
    position = Column(String, nullable=False)
    meta = Column(String, nullable=True)
    manager_id = Column(Integer, nullable=True)
    name_of_unit = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)