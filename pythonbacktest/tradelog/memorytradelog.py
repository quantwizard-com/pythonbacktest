from . import *


class MemoryTradeLog(AbstractTradeLog):

    def __init__(self):
        AbstractTradeLog.__init__(self)

    def log_transaction(self, price_bar_index_per_day, price_bar_time_stamp, transaction_type, shares_amount, transaction_price_per_share,
                        cash_spent, cash_after, position_after, all_indicators_values, comment=None):

        new_transaction_record = TransactionRecord()
        new_transaction_record.timestamp = price_bar_time_stamp
        new_transaction_record.price_bar_index_per_day = price_bar_index_per_day
        new_transaction_record.transaction_type = transaction_type
        new_transaction_record.shares_amount = shares_amount
        new_transaction_record.transaction_price_per_share = transaction_price_per_share
        new_transaction_record.cash_spent = cash_spent
        new_transaction_record.cash_after = cash_after
        new_transaction_record.position_after = position_after
        new_transaction_record.comment = comment
        new_transaction_record.total_assets = cash_after + position_after * transaction_price_per_share
        new_transaction_record.all_indicators_values = all_indicators_values

        self.all_transactions.append(new_transaction_record)



