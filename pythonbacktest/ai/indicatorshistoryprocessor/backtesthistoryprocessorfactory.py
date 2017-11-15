from pythonbacktest.ai.backoffice.backtestbackoffice.backofficefactory import BackOfficeFactory
from pythonbacktest.ai.indicatorshistoryprocessor.indicatorshistoryprocessor import IndicatorsHistoryProcessor
from pythonbacktest.ai.nodemanager import NodesMap, NodesProcessor
from pythonbacktest.ai.transactionevaluator import EvaluatorFactory


class BacktestHistoryProcessorFactory(object):

    @staticmethod
    def create_processor_factory(indicators_history,
                                 nodes_map_definition,
                                 evaluator_map,
                                 back_test_back_office):
        nodes_map = NodesMap(nodes_map_definition=nodes_map_definition)
        nodes_processor = NodesProcessor(nodes_map)

        evaluator_factory = EvaluatorFactory()
        evaluator = evaluator_factory.create_evaluator(evaluator_map=evaluator_map)

        return IndicatorsHistoryProcessor(indicators_history, nodes_processor, evaluator, back_test_back_office)
