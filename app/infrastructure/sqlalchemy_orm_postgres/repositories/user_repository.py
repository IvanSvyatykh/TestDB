import time
from logging import getLogger
from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.sqlalchemy_orm_postgres.models import UserTable
from domain.aggregates.user import User
from domain.value_object.money import Money
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects import postgresql


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy ORM logger")

    async def add_user(self, user: User) -> int:

        try:
            stmt = insert(UserTable).values(
                name=user.user_name, money=user.money.amount
            )
            self.__logger.debug(
                f"ORM compile this SQL query : {str(
                    stmt.compile(
                        dialect=postgresql.dialect(),
                        compile_kwargs={"literal_binds": True},
                    )
                )}"
            )
            await self.__session.execute(stmt)
            await self.__session.commit()
        except IntegrityError as e:
            await self.__session.rollback()
            self.__logger.error(e)
            raise e

    async def get_users(self) -> list[User]:
        try:
            start = time.time()
            stmt = select(UserTable)
            self.__logger.debug(
                f"ORM compile this SQL query : {str(
                    stmt.compile(
                        dialect=postgresql.dialect(),
                        compile_kwargs={"literal_binds": True},
                    )
                )}"
            )
            res = await self.__session.execute(stmt)
            users = list(res.scalars().all())
            end = time.time()
            self.__logger.debug(
                f"SQLAlchemy query with ORM took {end - start} seconds."
            )
            return (
                []
                if len(users) == 0
                else [
                    User(name=u.name, user_id=u.id, money=Money(u.money)) for u in users
                ]
            )
        except Exception as e:
            self.__logger.error(e)
            raise e
