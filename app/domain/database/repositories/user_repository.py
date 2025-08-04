from abc import ABC , abstractmethod



class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_users(self) -> list[User]:
        raise NotImplementedError
    @abstractmethod