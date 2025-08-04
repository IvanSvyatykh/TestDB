from abc import ABC, abstractmethod


class DatabaseConnector(ABC):

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    async def get_session(self):
        raise NotImplementedError
