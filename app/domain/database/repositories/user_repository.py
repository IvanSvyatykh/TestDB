from abc import ABC, abstractmethod
from domain.aggregates.user import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_users(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, user: User) -> int:
        raise NotImplementedError
