from logging import getLogger
from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.sqlalchemy_orm_postgres.models import User
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy ORM logger")

    async def add_user(self, user: User):

        try:
            await  self.__session.execute(insert(User).values(name=user.name, money=user.money))
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
            self.__logger.error(e)
            raise e
