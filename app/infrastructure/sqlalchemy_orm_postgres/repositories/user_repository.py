from logging import getLogger
from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.sqlalchemy_orm_postgres.models import UserTable
from domain.aggregates.user import User
from domain.value_object.money import Money
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy ORM logger")

    async def add_user(self, user: User):

        try:
            await self.__session.execute(
                insert(UserTable).values(name=user.user_name, money=user.money.amount)
            )
            await self.__session.commit()
        except IntegrityError as e:
            await self.__session.rollback()
            self.__logger.error(e)
            raise e

    async def get_users(self) -> list[User]:
        try:
            res = await self.__session.execute(select(UserTable))
            users = list(res.scalars().all())
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
