from domain.database.repositories.user_repository import UserRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from sqlalchemy import text
from infrastructure.sqlalchemy_orm_postgres.models import UserTable


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__logger = getLogger("User SQLAlchemy logger")

    async def get_users(self) -> list[UserTable]:
        query = text("SELECT * FROM users")
        try:
            res = await self.__session.execute(query)
            rows = res.fetchall()
        except Exception as e:
            self.__logger.error(e)
            raise e

    async def add_user(self, user: UserTable) -> int:
        pass
