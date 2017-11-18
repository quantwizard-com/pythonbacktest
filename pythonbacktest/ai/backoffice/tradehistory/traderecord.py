from typing import Text

from pythonbacktest.datafeed import PriceBar


class TradeRecord(object):
    __trigger_price_bar: PriceBar = None
    __transaction_type: Text = None
    __transaction_size = None
    __price_per_share = None
    __gross_transaction_cost = None
    __net_transaction_cost = None
    __broker_fee = None
    __tax = None
    __current_budget = None

    def __init__(self, trigger_price_bar: PriceBar, transaction_type,
                 transaction_size, price_per_share, current_budget,
                 gross_transaction_cost, net_transaction_cost,
                 broker_fee, tax):
        self.__trigger_price_bar = trigger_price_bar
        self.__transaction_type = transaction_type
        self.__transaction_size = transaction_size
        self.__price_per_share = price_per_share
        self.__gross_transaction_price = gross_transaction_cost
        self.__net_transaction_price = net_transaction_cost
        self.__current_budget = current_budget
        self.__broker_fee = broker_fee
        self.__tax = tax

    @property
    def trigger_price_bar(self):
        return self.__trigger_price_bar

    @property
    def transaction_type(self):
        """
        Type of the transaction. Possible values:
        - BUY
        - SELL
        - SSELL
        :return:
        """

        return self.__transaction_type

    @property
    def transaction_size(self):
        return self.__transaction_size

    @property
    def price_per_share(self):
        return self.__price_per_share

    @property
    def gross_transaction_cost(self):
        return self.__gross_transaction_cost

    @property
    def net_transaction_cost(self):
        return self.__net_transaction_cost

    @property
    def broker_fee(self):
        return self.__broker_fee

    @property
    def tax(self):
        return self.__tax

