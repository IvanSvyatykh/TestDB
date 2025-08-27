from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncEngine


class DatabaseMigrator(ABC):

    @abstractmethod
    async def create_table(self, table_name: str) -> None:
        raise NotImplementedError
