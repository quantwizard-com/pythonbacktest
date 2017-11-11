from ai.indicatorshistoryprocessor.indicatorshistoryprocessor import IndicatorsHistoryProcessor
from ai.nodemanager import NodesMap, NodesProcessor
from ai.tradeexecutor import BackTestTradeExecutor
from ai.transactionevaluator import EvaluatorFactory


class BacktestHistoryProcessorFactory(object):

    def create_processor_factory(self, indicators_history, nodes_map_definition, evaluator_map):
        nodes_map = NodesMap(nodes_map_definition=nodes_map_definition)
        nodes_processor = NodesProcessor(nodes_map)

        evaluator_factory = EvaluatorFactory()
        evaluator = evaluator_factory.create_evaluator(evaluator_map=evaluator_map)

        trade_executor = BackTestTradeExecutor()

        return IndicatorsHistoryProcessor(indicators_history, nodes_processor, evaluator, trade_executor)
