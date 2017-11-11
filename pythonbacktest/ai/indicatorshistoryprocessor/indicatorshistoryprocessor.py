from pythonbacktest.ai.nodemanager import NodesProcessor
from pythonbacktest.ai.tradeexecutor import AbstractTradeExecutor
from pythonbacktest.ai.transactionevaluator import Evaluator
from pythonbacktest.indicatorshistory import IndicatorHistory


class IndicatorsHistoryProcessor(object):

    def __init__(self, indicators_history: IndicatorHistory, nodes_processor: NodesProcessor,
                 transaction_evaluator: Evaluator, trade_executor: AbstractTradeExecutor):
        self.__indicators_history = indicators_history
        self.__nodes_processor = nodes_processor
        self.__transaction_evaluator = transaction_evaluator
        self.__trade_executor = trade_executor

    def run_processor(self):
        for time_stamp, snapshot in self.__indicators_history.all_snapshots.items():

            nodes_results = self.__nodes_processor.new_indicators_snapshot(snapshot)

            