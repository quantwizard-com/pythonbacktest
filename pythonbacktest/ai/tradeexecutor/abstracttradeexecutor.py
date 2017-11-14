from abc import ABC, abstractmethod
from typing import Text

from pythonbacktest.ai.tradehistory.tradehistory import TradeHistory


class AbstractTradeExecutor(ABC):
    def __init__(self, trade_history: TradeHistory):
        self.TRANSACTION_NAME_TO_FUNCTION = {
            "buy": self.buy,
            "sell": self.sell,
            "ssell": self.short_sell
        }

        self.__trade_history = trade_history

    def execute_transaction(self, transaction_name: Text, order_size):
        if not transaction_name:
            raise ValueError("Empty transaction_name passed to the function")

        transaction_name = transaction_name.lower()
        if transaction_name not in self.TRANSACTION_NAME_TO_FUNCTION:
            raise ValueError(f"Unknown transaction name: {transaction_name}")

        self.TRANSACTION_NAME_TO_FUNCTION[transaction_name](order_size)

    @property
    def trade_history(self):
        return self.__trade_history

    @abstractmethod
    def buy(self, order_size):
        raise NotImplementedError()

    @abstractmethod
    def sell(self, order_size):
        raise NotImplementedError()

    @abstractmethod
    def short_sell(self, order_size):
        raise NotImplementedError()
