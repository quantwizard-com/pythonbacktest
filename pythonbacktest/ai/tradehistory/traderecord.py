from typing import Text


class TradeRecord(object):
    timestamp = None
    transaction_type: Text = None
    transaction_size = None
    unit_price = None
    broker_fee = None
    tax = None
    current_budget = None

    def __init__(self, timestamp, transaction_type, transaction_size, unit_price, current_budget, broker_fee, tax):
        self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.transaction_size = transaction_size
        self.unit_price = unit_price
        self.current_budget = current_budget
        self.broker_fee = broker_fee
        self.tax = tax

