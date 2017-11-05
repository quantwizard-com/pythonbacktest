from abc import ABC, abstractmethod
from typing import Text


class AbstractTradeExecutor(ABC):
    def __init__(self):
        self.TRANSACTION_NAME_TO_FUNCTION = {
            "buy": self.buy,
            "sell": self.sell,
            "ssell": self.ssell
        }

    def execute_transaction(self, transaction_name: Text):
        transaction_name = transaction_name.lower()
        if transaction_name not in self.TRANSACTION_NAME_TO_FUNCTION:
            raise ValueError(f"Unknown transaction name: {transaction_name}")

        self.TRANSACTION_NAME_TO_FUNCTION[transaction_name]()

    @abstractmethod
    def buy(self):
        raise NotImplementedError()

    @abstractmethod
    def sell(self):
        raise NotImplementedError()

    @abstractmethod
    def ssell(self):
        raise NotImplementedError()
