import os, sys, inspect, random

# realpath() will make your script run, even if you symlink it :)

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
python_backtest_path = os.path.abspath(cmd_folder + '/../../')
sys.path.insert(0, python_backtest_path)

from pythonbacktest.datafeed import DBDataFeed
from pythonbacktest.indicator import SMA, DataCrossIndicator, DataDifference
from pythonbacktest.indicatorcalculator import IndicatorsCalculator
from pythonbacktest.indicatorcalculator import IndicatorsMap
from pythonbacktest.indicatorshistory import IndicatorHistory, ReferencialSnapshot, AbstractSnapshot
from pythonbacktest.ai.backoffice.backtestbackoffice.backofficefactory import BackOfficeFactory
from pythonbacktest.ai.nodes import FunctionalNode
from pythonbacktest.ai.indicatorshistoryprocessor.backtesthistoryprocessorfactory import BacktestHistoryProcessorFactory
from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.ai.strategyperformance.calculators.buysellperfcalculator import BuySellPerfCalculator

SECURITY_SYMBOL = 'MSFT'

########################################################################################################################
#######                                          DOWNLOAD DATA                                                   #######
########################################################################################################################

db_data_feed = DBDataFeed()
DATES_TO_ANALYSIS = db_data_feed.get_dates_for_symbol_min_data(SECURITY_SYMBOL, 4670)

# get data for the random date
single_date = random.choice(DATES_TO_ANALYSIS)
price_bars = db_data_feed.get_prices_bars_for_day_for_symbol(single_date, SECURITY_SYMBOL)


########################################################################################################################
#######                                      DEFINE INDICATORS MAP                                               #######
########################################################################################################################
# calculate indicators for the selected date
indicators_map_definition = [
    {'sources': 'close', 'implementation': SMA(indicator_name='SMA_50', window_len=50)},
    {'sources': 'close', 'implementation': SMA(indicator_name='SMA_200', window_len=200)},
    {'sources': ['SMA_50', 'SMA_200'], 'implementation': DataDifference(indicator_name='SMA_DIFFERENCE')},
    {'sources': ['SMA_50', 'SMA_200'], 'implementation': DataCrossIndicator(indicator_name='SMA_CROSS')},
]

indicators_map = IndicatorsMap(indicators_map_definition=indicators_map_definition)


########################################################################################################################
#######                                         RUN CALCULATIONS                                                 #######
########################################################################################################################
indicators_history = IndicatorHistory(ReferencialSnapshot)
indicators_calculator = IndicatorsCalculator(indicators_map, target_indicators_history=indicators_history)
indicators_calculator.run_calculation(price_bars)

print(indicators_history.last_snapshot)


########################################################################################################################
#######                                        NODE MAP DEFINITION                                               #######
########################################################################################################################
def sma_diff_node_func(indicators_source: AbstractSnapshot, trade_data_snapshot: TradeDataSnapshot):
    sma_difference = indicators_source['SMA_DIFFERENCE']
    if sma_difference:
        return sma_difference > 0

    # no processable data available
    return None


def sma_cross_node(indicators_snapshot: AbstractSnapshot, trade_data_snapshot: TradeDataSnapshot):
    sma_cross = indicators_snapshot['SMA_CROSS']
    if sma_cross:
        return sma_cross == 1

    # no processable data available
    return None


def current_position_node(indicators_snapshot: AbstractSnapshot, trade_data_snapshot: TradeDataSnapshot):
    return trade_data_snapshot.current_position_size > 0



nodes_map_definition = [
    {'nodeimplementation': FunctionalNode('sma_diff_node', function_to_call=sma_diff_node_func)},
    {'nodeimplementation': FunctionalNode('sma_cross_node', function_to_call=sma_cross_node)},
    {'nodeimplementation': FunctionalNode('position_node', function_to_call=current_position_node)},
]

evaluator_map = {
    "buy": ["sma_diff_node", "sma_cross_node", "!position_node"],
    "sell": ["!sma_diff_node", "sma_cross_node", "position_node"],
    "ssell": None
}

back_test_back_office = BackOfficeFactory.create_back_test_back_office(
    initial_budget=10000, default_transaction_size=100,
    apply_tax=False, apply_broker_fees=False)

performance_calculator = BuySellPerfCalculator()

history_processor = BacktestHistoryProcessorFactory.create_processor_factory(
    indicators_history=indicators_history,
    nodes_map_definition=nodes_map_definition,
    evaluator_map=evaluator_map,
    back_test_back_office=back_test_back_office,
    performance_calculator=performance_calculator)

performance_report = history_processor.run_processor()

print(back_test_back_office.trade_history.trade_records)
print(performance_report)



