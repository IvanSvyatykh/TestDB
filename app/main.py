import asyncio
import logging
import sys
import uuid
import colorlog
from infrastructure.sqlalchemy_orm_postgres.models import UserTable
from domain.database.repositories.user_repository import UserRepositoryInterface
from infrastructure.sqlalchemy_orm_postgres.repositories.user_repository import (
    UserRepository as UserRepoasitoryORM,
)
from infrastructure.sqlalchemy_postgres.repositories.user_repository import (
    UserRepository,
)
from domain.aggregates.user import User
from domain.value_object.money import Money
from domain.database.migrator import DatabaseMigrator
from domain.database.connector import DatabaseConnector
from infrastructure.sqlalchemy_orm_postgres.migrator import PostgresMigrator
from infrastructure.sqlalchemy_orm_postgres.connector import PostgresConnector
from domain.database.repositories.user_repository import UserRepositoryInterface
from config import DATABASE_URL


handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[handler],
)


async def get_users(
    logger: logging.Logger, user_repository: UserRepositoryInterface
) -> None:
    logger.info("Getting users from db...")
    try:
        users = await user_repository.get_users()
        logger.info(
            f"Get users: {[ (user.user_id , user.user_name , user.money.amount) for user in users]}"
        )
    except Exception as e:
        logger.error(f"Can not get user due err!")
        logger.error(f"Get err {str(e)}")
        sys.exit()


async def add_user(
    logger: logging.Logger, user_repository: UserRepositoryInterface
) -> None:
    user = User(name=str(uuid.uuid4()), money=Money(1000.39))
    logger.info("Starting add user to db...")
    try:
        await user_repository.add_user(user)
        logger.info("User succesfully added!")
    except Exception as e:
        logger.error(f"Can not add user to db due {str(e)}")


async def start_connection(
    logger: logging.Logger, database_url: str
) -> DatabaseConnector:
    connector = PostgresConnector(database_url)
    try:
        await connector.connect()
        logger.info(f"Successfully connect to {database_url}.")
        return connector
    except Exception as e:
        logger.error(f"Can not connect to {database_url} !")
        logger.error(f"Get err {str(e)}")
        logger.info("Script aborted !")
        sys.exit()


async def main(database_url: str):
    logger = logging.getLogger("Test task logger")
    logger.info("Script started !")

    connector = await start_connection(logger, database_url)
    migrator = PostgresMigrator(connector.get_engine)

    await migrator.create_table(UserTable.__tablename__)
    async with connector.get_session() as session:
        user_repo_orm = UserRepoasitoryORM(session)
        user_repo = UserRepository(session)

        await get_users(logger, user_repo)
        await get_users(logger, user_repo_orm)

        await add_user(logger, user_repo)
        await add_user(logger, user_repo)

        await get_users(logger, user_repo)
        await get_users(logger, user_repo_orm)
    await connector.disconnect()
    logger.info("Close connection!")


if __name__ == "__main__":
    asyncio.run(main(DATABASE_URL))
