from pythonbacktest.ai.indicatorshistoryprocessor.singleday.indicatorshistoryprocessor import IndicatorsHistoryProcessor
from pythonbacktest.ai.nodemanager import NodesMap, NodesProcessor
from pythonbacktest.ai.strategyperformance.singleday.calculators.abstractperfcalculator import AbstractPerfCalculator
from pythonbacktest.ai.transactionevaluator import EvaluatorFactory


class BacktestHistoryProcessorFactory(object):

    @staticmethod
    def create_indicators_history_processor(indicators_history,
                                            nodes_map_definition,
                                            evaluator_map,
                                            back_test_back_office,
                                            performance_calculator: AbstractPerfCalculator):
        nodes_map = NodesMap(nodes_map_definition=nodes_map_definition)
        nodes_processor = NodesProcessor(nodes_map)

        evaluator_factory = EvaluatorFactory()
        evaluator = evaluator_factory.create_evaluator(evaluator_map=evaluator_map)

        return IndicatorsHistoryProcessor(
            indicators_history, nodes_processor,
            evaluator, back_test_back_office, performance_calculator)
