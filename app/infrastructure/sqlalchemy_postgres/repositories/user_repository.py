import time
from logging import getLogger

from domain.aggregates.user import User
from domain.database.repositories.user_repository import \
    UserRepositoryInterface
from domain.value_object.money import Money
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy logger")

    async def get_users(self) -> list[User]:
        query = text("SELECT * FROM users")
        try:
            start = time.time()
            res = await self.__session.execute(query)
            rows = res.fetchall()
            end = time.time()
            self.__logger.debug(
                f"SQLAlchemy query with raw SQL took {end - start} seconds."
            )
            return (
                []
                if len(rows) == 0
                else [
                    User(user_id=r[0], name=r[1], money=Money(amount=r[2]))
                    for r in rows
                ]
            )
        except Exception as e:
            self.__logger.error(e)
            raise e

    async def add_user(self, user: User) -> int:

        try:
            query = text(
                f"INSERT INTO users (name, money) VALUES (:name,:money);"
            ).bindparams(name=user.user_name, money=user.money.amount)
            await self.__session.execute(query)
            await self.__session.commit()
        except IntegrityError as e:
            await self.__session.rollback()
            self.__logger.error(e)
            raise e
