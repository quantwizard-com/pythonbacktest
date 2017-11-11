from typing import Text, List

from .traderecord import TradeRecord


class TradeHistory(object):

    def __init__(self, initial_budget):
        self.__current_budget = initial_budget

        self.__trade_records: List[TradeRecord] = []

    @property
    def current_budget(self):
        return self.__current_budget

    @property
    def trade_records(self):
        return self.__trade_records

    def new_transaction(self, timestamp, transaction_type: Text, transaction_size, unit_price, broker_fee=0, tax=0):
        trade_record = TradeRecord(timestamp, transaction_type, transaction_size,
                                   unit_price, self.__current_budget, broker_fee, tax)
        self.__trade_records.append(trade_record)


