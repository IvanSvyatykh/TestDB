from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from logging import  getLogger
from typing import Coroutine
from infrastructure.sqlalchemy_orm_postgres.models import User


class UserRepository(UserRepositoryInterface):

    def __init__(self,session:AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy logger")


    async def get_users(self) -> list[User]:
        pass

    async def add_user(self, user: User)->int:
        pass

