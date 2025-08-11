from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy import text
from domain.aggregates.user import User
from domain.value_object.money import Money


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy logger")

    async def get_users(self) -> list[User]:
        query = text("SELECT * FROM users")
        try:
            res = await self.__session.execute(query)
            rows = res.fetchall()
            return (
                []
                if len(rows)  == 0
                else [User(user_id=r[0], name=r[1], money=Money(amount=r[2])) for r in rows]
            )
        except Exception as e:
            self.__logger.error(e)
            raise e

    async def add_user(self, user: User) -> int:
        pass
