import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
from ai.nodemanager import NodesMap
from ai.nodes import FunctionalNode

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
python_backtest_path = os.path.abspath(cmd_folder + '/../../')
sys.path.insert(0, python_backtest_path)

from pythonbacktest.ai.utils.indicatorshistorysource import IndicatorsHistorySource
from pythonbacktest.datafeed import DBDataFeed
from pythonbacktest.indicator import SMA, DataCrossIndicator, DataDifference
from pythonbacktest.indicatorcalculator import IndicatorsCalculator
from pythonbacktest.indicatorcalculator import IndicatorsMap
from pythonbacktest.indicatorshistory import IndicatorHistory, ReferencialSnapshot

import random

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
def sma_diff_node_func(indicators_source: IndicatorsHistorySource):
    sma_difference = indicators_source['SMA_DIFFERENCE']
    if sma_difference:
        return sma_difference > 0

    # no processable data available
    return None


def sma_cross_node(indicators_source: IndicatorsHistorySource):
    sma_cross = indicators_source['SMA_CROSS']
    if sma_cross:
        return sma_cross == 1

    # no processable data available
    return None


nodes_map_definition = [
    { 'nodeimplementation': FunctionalNode('sma_diff_node', function_to_call=sma_diff_node_func)}
]

indicators_history_source = IndicatorsHistorySource(indicators_history=indicators_history)
nodes_map = NodesMap(nodes_map_definition=nodes_map_definition, indicators_history=indicators_history)


