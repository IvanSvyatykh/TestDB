import logging

from domain.database.migrator import DatabaseMigrator
from infrastructure.sqlalchemy_orm_postgres.models import Base
from sqlalchemy import inspect


class PostgresMigrator(DatabaseMigrator):
    def __init__(self, engine):
        self.__logger = logging.getLogger("Postgres migrator logger")
        self.__engine = engine

    async def __is_table_exists(self, table_name: str) -> bool:
        async with self.__engine.connect() as conn:
            return await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).has_table(table_name)
            )

    async def create_table(self, table_name: str) -> None:
        if not await self.__is_table_exists(table_name):
            async with self.__engine.begin() as conn:
                await conn.run_sync(
                    lambda sync_conn: Base.metadata.create_all(
                        bind=sync_conn, tables=[Base.metadata.tables[table_name]]
                    )
                )
            self.__logger.info(f"Table {table_name} created")
        else:
            self.__logger.warning(f"Table {table_name} already exists")
