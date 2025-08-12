import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncEngine
from dataclasses import dataclass
from domain.database.migrator import DatabaseMigrator


@dataclass
class TableDefinition:
    name: str
    columns: Dict[str, str]
    primary_key: str = None
    foreign_keys: Dict[str, Any] = None
    indexes: Dict[str, Any] = None


class PostgresRawSQLMigrator(DatabaseMigrator):
    def __init__(self, engine: AsyncEngine):
        self.__logger = logging.getLogger("PostgresRawSQL migrator logger")
        self.__engine = engine

    async def __is_table_exists(self, table_name: str) -> bool:
        async with self.__engine.connect() as conn:
            result = await conn.execute(
                f"""
                SELECT EXISTS (
                    SELECT FROM pg_tables
                    WHERE schemaname = 'public'
                    AND tablename = '{table_name}'
                );
                """
            )
            return result.scalar()

    def __generate_create_table_sql(self, table_def: TableDefinition) -> str:
        columns_sql = []
        for name, definition in table_def.columns.items():
            columns_sql.append(f"{name} {definition}")

        if table_def.primary_key:
            columns_sql.append(f"PRIMARY KEY ({table_def.primary_key})")

        if table_def.foreign_keys:
            for column, fk_def in table_def.foreign_keys.items():
                columns_sql.append(
                    f"FOREIGN KEY ({column}) REFERENCES {fk_def['references']}"
                )
        sql = f"""
        CREATE TABLE {table_def.name} (
            {', '.join(columns_sql)}
        );
        """

        if table_def.indexes:
            for index_name, columns in table_def.indexes.items():
                if isinstance(columns, str):
                    columns = [columns]
                sql += f"\nCREATE INDEX {index_name} ON {table_def.name} ({', '.join(columns)};"

        return sql

    async def create_table(self, table_def: TableDefinition) -> None:
        if not await self.__is_table_exists(table_def.name):
            async with self.__engine.begin() as conn:
                create_sql = self.__generate_create_table_sql(table_def)
                self.__logger.debug(f"Executing SQL:\n{create_sql}")
                await conn.execute(create_sql)
            self.__logger.info(f"Table {table_def.name} created")
        else:
            self.__logger.warning(f"Table {table_def.name} already exists")

    async def drop_table(self, table_name: str) -> None:
        if await self.__is_table_exists(table_name):
            async with self.__engine.begin() as conn:
                await conn.execute(f"DROP TABLE {table_name} CASCADE;")
            self.__logger.info(f"Table {table_name} dropped")
        else:
            self.__logger.warning(f"Table {table_name} doesn't exist")
