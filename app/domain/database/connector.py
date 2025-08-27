from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseConnector(ABC):

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        raise NotImplementedError

    @property
    @abstractmethod
    def get_engine(self) -> Any:
        raise NotImplementedError
