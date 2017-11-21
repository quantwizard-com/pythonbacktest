from collections import OrderedDict
from typing import Dict

from pythonbacktest.ai.strategyperformance.multiday import MultidayPerformanceCalculator
from pythonbacktest.ai.backoffice.backtestbackoffice.backofficefactory import BackOfficeFactory
from pythonbacktest.ai.indicatorshistoryprocessor.singleday import BacktestHistoryProcessorFactory
from pythonbacktest.ai.strategyperformance.singleday.calculators.abstractperfcalculator import AbstractPerfCalculator
from pythonbacktest.indicatorcalculator import IndicatorsMap, IndicatorsCalculator
from pythonbacktest.indicatorshistory import IndicatorHistory, ReferencialSnapshot


class MultidayHistoryProcessor(object):

    def __init__(self, multiday_data: OrderedDict, indicators_map_definition: Dict,
                 nodes_map_definition, evaluator_map, performance_calculator: AbstractPerfCalculator,
                 initial_budget, default_transaction_size):

        self.__multiday_data = multiday_data
        self.__indicators_map_definition = indicators_map_definition
        self.__nodes_map_definition = nodes_map_definition
        self.__evaluator_map = evaluator_map
        self.__performance_calculator = performance_calculator
        self.__initial_budget = initial_budget
        self.__default_transaction_size = default_transaction_size

    def run_processor(self) -> OrderedDict:
        multiday_performance_report = OrderedDict()

        for date, price_bars in self.__multiday_data.items():

            # calculate indicators history
            indicators_history = self.__calculate_history(price_bars=price_bars)

            # get the performance report for the single day
            multiday_performance_report[date] = self.__run_back_office_get_performance_report(indicators_history)

        return MultidayPerformanceCalculator.calculate_multiday_performance_report(multiday_performance_report)

    def __calculate_history(self, price_bars):
        indicators_map = IndicatorsMap(indicators_map_definition=self.__indicators_map_definition)
        indicators_history = IndicatorHistory(ReferencialSnapshot)
        indicators_calculator = IndicatorsCalculator(indicators_map, target_indicators_history=indicators_history)
        indicators_calculator.run_calculation(price_bars=price_bars)

        return indicators_history

    def __run_back_office_get_performance_report(self, indicators_history):
        back_test_back_office = BackOfficeFactory.create_back_test_back_office(
            initial_budget=self.__initial_budget, default_transaction_size=self.__default_transaction_size)

        history_processor = BacktestHistoryProcessorFactory.create_indicators_history_processor(
            indicators_history=indicators_history,
            nodes_map_definition=self.__nodes_map_definition,
            evaluator_map=self.__evaluator_map,
            back_test_back_office=back_test_back_office,
            performance_calculator=self.__performance_calculator)

        return history_processor.run_processor()




