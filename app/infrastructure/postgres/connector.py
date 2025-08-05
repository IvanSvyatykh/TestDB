from contextlib import asynccontextmanager
from domain.database.connector import DatabaseConnector
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, AsyncConnection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import Any, AsyncGenerator


class PostgresConnector(DatabaseConnector):

    def __init__(self, database_url: str):
        self.__engine = None
        self.__async_session_generator = None
        self.__database_url = database_url

    async def connect(self):
        self.__engine = create_async_engine(self.__database_url, pool_size=10,
                                            max_overflow=20, )
        self.__async_session_generator = async_sessionmaker(self.__engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__async_session_generator() as session:
            try:
                yield session
            finally:
                await session.close()

    @property
    def get_engine(self)->Any:
        return self.__engine

    async def disconnect(self):
        await self.__engine.dispose()
