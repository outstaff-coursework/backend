from sqlalchemy import Column
from sqlalchemy import String
from base_db_engine import Base


class Calendar(Base):
    __tablename__ = "calendars"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    calendar_url = Column(String, nullable=False)