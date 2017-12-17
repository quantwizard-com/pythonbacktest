from typing import Text, List

from pythonbacktest.datafeed import PriceBar
from .traderecord import TradeRecord


class TradeHistory(object):

    def __init__(self):
        self.__trade_records: List[TradeRecord] = []

        # list of price bar timestamps which triggered individual trades
        # this is used for duplicate transaction records
        self.__trade_records_timestamps = []

    @property
    def trade_records(self):
        return self.__trade_records

    def new_transaction(self, trigger_price_bar: PriceBar, transaction_type: Text,
                        transaction_size, price_per_share, current_budget,
                        gross_transaction_cost, net_transaction_cost, broker_fee=0, tax=0):

        trade_timestamp = trigger_price_bar.timestamp

        if trade_timestamp in self.__trade_records_timestamps:
            raise ValueError(f"Timestamp {trade_timestamp} already recorded.")

        trade_record = TradeRecord(trigger_price_bar, transaction_type, transaction_size,
                                   price_per_share, current_budget,
                                   gross_transaction_cost,net_transaction_cost,
                                   broker_fee, tax)
        self.__trade_records.append(trade_record)
        self.__trade_records_timestamps.append(trade_timestamp)


