from typing import Text, List

from datafeed import PriceBar
from .traderecord import TradeRecord


class TradeHistory(object):

    def __init__(self):
        self.__trade_records: List[TradeRecord] = []

    @property
    def trade_records(self):
        return self.__trade_records

    def new_transaction(self, trigger_price_bar: PriceBar, transaction_type: Text,
                        transaction_size, price_per_share, current_budget,
                        gross_transaction_cost, net_transaction_cost, broker_fee=0, tax=0):

        trade_record = TradeRecord(trigger_price_bar, transaction_type, transaction_size,
                                   price_per_share, current_budget,
                                   gross_transaction_cost,net_transaction_cost,
                                   broker_fee, tax)
        self.__trade_records.append(trade_record)


