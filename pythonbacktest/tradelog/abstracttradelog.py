import abc


class AbstractTradeLog(object):

    def __init__(self):
        pass

    # log transaction for the trade; parameters
    # - price_bar_time_stamp - timestamp on the
    # - transaction_type - BUY/SALE/SHORT
    # - shares_amount - number of shares traded
    # -
    @abc.abstractmethod
    def log_transaction(self, price_bar_index_per_day, price_bar_time_stamp, transaction_type, shares_amount, transaction_price_per_share,
                        cash_spent, cash_after, position_after):
        raise NotImplementedError()
