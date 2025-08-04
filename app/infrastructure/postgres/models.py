import uuid

from sqlalchemy import (
    Column,
    String,
    UUID,
    Float
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(256), index=True, unique=True)
    # Для простоты примера де нормализуем таблицу
    money = Column(Float(precision=2))
