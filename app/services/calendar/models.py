from sqlalchemy import Column
from sqlalchemy import String
from base_db_engine import Base


class Calendar(Base):
    __tablename__ = "calendars"

    username = Column(String, unique=True, primary_key=True, nullable=False)
    calendar_url = Column(String, nullable=False)