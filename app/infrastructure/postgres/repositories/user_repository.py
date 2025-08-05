from typing import AsyncGenerator
from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.postgres.models import User
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add_user(self, user: User):


            try:
                await  self.__session.execute(insert(User).values(id=user.id, name=user.name, money=user.money))
                await  self.__session.commit()
            except IntegrityError as e:
                await  self.__session.rollback()
                raise e

    async def get_users(self) -> list[User]:
            try:
                res = await  self.__session.execute(select(User))
                users = res.scalars().all()
                return list(users)
            except Exception as e:
                print(str(e))
