from decimal import Decimal, getcontext


class Money:

    def __init__(self, amount: float) -> None:
        getcontext().prec = 8
        self.__amount = Decimal(amount)

    @property
    def amount(self) -> Decimal:
        return self.__amount
