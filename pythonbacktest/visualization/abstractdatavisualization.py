import abc


class AbstractDataVisualization(object):

    def __init__(self):
        self.__indicators_history = None
        self.__indicators_name_collections = None
        self.__recorded_transaction_names = []

        self.__trade_transactions = {}

    def add_indicators_history(self, indicators_history, *indicators_name_collections):
        self.__indicators_history = indicators_history
        self.__indicators_name_collections = indicators_name_collections

    def add_transactions_from_trade_log(self, trade_log, *transaction_names):

        self.__recorded_transaction_names = list(transaction_names)
        for trade_record in trade_log.all_transactions:
            transaction_type = trade_record.transaction_type
            transaction_price_per_share = trade_record.transaction_price_per_share
            price_bar_index = trade_record.price_bar_index_per_day

            if transaction_type in transaction_names:
                if transaction_type in self.__trade_transactions:
                    self.__trade_transactions[transaction_type].append((price_bar_index, transaction_price_per_share))
                else:
                    self.__trade_transactions[transaction_type] = list([(price_bar_index, transaction_price_per_share)])

    @property
    def trade_transactions(self):
        return self.__trade_transactions

    @property
    def recorded_transaction_names(self):
        return self.__recorded_transaction_names

    @property
    def indicators_name_collections(self):
        return self.__indicators_name_collections

    @property
    def indicators_history(self):
        return self.__indicators_history
