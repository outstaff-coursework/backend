from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from base_db_engine import Base


class Auth(Base):
    __tablename__ = "auth"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String, index=True)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean)
