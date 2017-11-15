from pythonbacktest.ai.backoffice.backtestbackoffice.backofficefactory import BackOfficeFactory
from pythonbacktest.ai.indicatorshistoryprocessor.indicatorshistoryprocessor import IndicatorsHistoryProcessor
from pythonbacktest.ai.nodemanager import NodesMap, NodesProcessor
from pythonbacktest.ai.transactionevaluator import EvaluatorFactory


class BacktestHistoryProcessorFactory(object):

    @staticmethod
    def create_processor_factory(indicators_history,
                                 nodes_map_definition,
                                 evaluator_map,
                                 transaction_size,
                                 initial_budget,
                                 apply_tax=True,
                                 apply_broker_fees=True):
        nodes_map = NodesMap(nodes_map_definition=nodes_map_definition)
        nodes_processor = NodesProcessor(nodes_map)

        evaluator_factory = EvaluatorFactory()
        evaluator = evaluator_factory.create_evaluator(evaluator_map=evaluator_map)

        back_test_back_office = BackOfficeFactory.create_back_test_back_office(
            initial_budget=initial_budget, default_transaction_size=transaction_size,
            apply_tax=apply_tax, apply_broker_fees=apply_broker_fees)

        return IndicatorsHistoryProcessor(indicators_history, nodes_processor, evaluator, back_test_back_office)
