from typing import Text

from pythonbacktest.datafeed import PriceBar


class TradeRecord(object):
    trigger_price_bar: PriceBar = None
    transaction_type: Text = None
    transaction_size = None
    price_per_share = None
    broker_fee = None
    tax = None
    current_budget = None

    def __init__(self, trigger_price_bar: PriceBar, transaction_type,
                 transaction_size, price_per_share, current_budget, broker_fee, tax):
        self.trigger_price_bar = trigger_price_bar
        self.transaction_type = transaction_type
        self.transaction_size = transaction_size
        self.price_per_share = price_per_share
        self.current_budget = current_budget
        self.broker_fee = broker_fee
        self.tax = tax

