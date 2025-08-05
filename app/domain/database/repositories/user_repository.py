from abc import ABC, abstractmethod
from infrastructure.postgres.models import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_users(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, user: User):
        raise NotImplementedError
