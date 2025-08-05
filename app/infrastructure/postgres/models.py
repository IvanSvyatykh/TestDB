import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric

)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(256), index=True, unique=True)
    # Для простоты примера де нормализуем таблицу
    money = Column(Numeric(precision=10,scale= 2))


