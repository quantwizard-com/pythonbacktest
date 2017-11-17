from datafeed import PriceBar
from pythonbacktest.ai.backoffice.backtestbackoffice.backtestbackoffice import BackTestBackOffice
from pythonbacktest.ai.nodemanager import NodesProcessor
from pythonbacktest.ai.transactionevaluator import Evaluator
from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.indicatorshistory import IndicatorHistory


class IndicatorsHistoryProcessor(object):

    def __init__(self, indicators_history: IndicatorHistory, nodes_processor: NodesProcessor,
                 transaction_evaluator: Evaluator, back_office: BackTestBackOffice):
        self.__indicators_history = indicators_history
        self.__nodes_processor = nodes_processor
        self.__transaction_evaluator = transaction_evaluator
        self.__back_office = back_office

    def run_processor(self):
        for time_stamp, snapshot in self.__indicators_history.all_snapshots.items():

            # Get and propagate current price bar
            current_price_bar = PriceBar(snapshot['pricebar'])
            self.__back_office.set_price_bar(current_price_bar)

            # calculate status of the nodes
            trade_data_snapshot = self.__back_office.trade_data_snapshot
            nodes_results = self.__nodes_processor.new_data_snapshots(snapshot, trade_data_snapshot)

            recommended_transaction = self.__transaction_evaluator.evaluate_new_nodes_values(nodes_results)

            if recommended_transaction:
                self.__back_office.execute_transaction(recommended_transaction)
