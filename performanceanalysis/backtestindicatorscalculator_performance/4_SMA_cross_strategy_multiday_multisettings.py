import inspect
import os
import sys

# realpath() will make your script run, even if you symlink it :)
from ai.indicatorshistoryprocessor.multiday.multidayhistoryprocessor import MultidayHistoryProcessor

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
python_backtest_path = os.path.abspath(cmd_folder + '/../../')
sys.path.insert(0, python_backtest_path)

from pythonbacktest.datafeed import DBDataFeed
from pythonbacktest.indicator import SMA, DataCrossIndicator, DataDifference
from pythonbacktest.indicatorshistory import AbstractSnapshot
from pythonbacktest.ai.nodes import FunctionalNode
from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.ai.strategyperformance.singleday.calculators.buysellperfcalculator import BuySellPerfCalculator

SECURITY_SYMBOL = 'MSFT'

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

db_data_feed = DBDataFeed()

for sma1 in range(10, 201, 10):
    for sma2 in range(sma1+10, 201, 10):

        print(f"sma1: {sma1}, sma2: {sma2}")

        indicators_map_definition = [
            {'sources': 'close', 'implementation': SMA(indicator_name='SMA_1', window_len=sma1)},
            {'sources': 'close', 'implementation': SMA(indicator_name='SMA_2', window_len=sma2)},
            {'sources': ['SMA_1', 'SMA_2'], 'implementation': DataDifference(indicator_name='SMA_DIFFERENCE')},
            {'sources': ['SMA_1', 'SMA_2'], 'implementation': DataCrossIndicator(indicator_name='SMA_CROSS')},
        ]

        # get data for the random date
        price_bars_per_date = db_data_feed.get_random_sample_of_valid_data_for_symbol(SECURITY_SYMBOL, 10)

        performance_calculator = BuySellPerfCalculator()

        multiday_history_processor = MultidayHistoryProcessor(
            indicators_map_definition=indicators_map_definition,
            nodes_map_definition=nodes_map_definition,
            evaluator_map=evaluator_map,
            performance_calculator=performance_calculator,
            initial_budget=10000,
            default_transaction_size=300)

        multiday_performance_report = multiday_history_processor.run_processor(multiday_data=price_bars_per_date)

        print(f"net pnl: {multiday_performance_report.total_net_pnl}, "
              f"std net pnl: {multiday_performance_report.std_net_pnl}")