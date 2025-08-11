from domain.value_object.money import Money


class User:

    def __init__(self, name: str, money: Money, user_id: int | None = None) -> None:
        self.__check_user_id(user_id)
        self.__user_id = user_id
        self.__name = name
        self.__money = money

    @property
    def user_name(self) -> str:
        return self.__name

    @property
    def money(self) -> Money:
        return self.__money

    @property
    def user_id(self) -> int:
        if self.__user_id is None:
            raise AttributeError("User has not been set yet")
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        self.__check_user_id(user_id)
        if user_id is None:
            raise AttributeError("User id cannot be None")
        self.__user_id = user_id

    def __check_user_id(self, user_id: int):
        if user_id <= 0:
            raise ValueError("User id must be greater than 0")
