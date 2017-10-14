from pythonbacktest.datafeed import DBDataFeed
from pythonbacktest.ai.nodes.specialists import DataCrossNode

from pythonbacktest.indicator import SMA

from pythonbacktest.indicatorcalculator import IndicatorHistory
from pythonbacktest.indicatorcalculator import IndicatorsCalculator
from pythonbacktest.indicatorcalculator import BacktestIndicatorsCalculator
from pythonbacktest.indicatorcalculator import IndicatorsCalculatorPerfMonitor
from pythonbacktest.indicatorcalculator import Utils

sma_range = range(10, 301, 10)

generated_values = []

for sma_value1 in sma_range:
    for sma_value2 in sma_range:
        if sma_value2 > sma_value1:
            generated_values.append(
                {'SMA_1': sma_value1, 'SMA_2': sma_value2}
            )

SECURITY_SYMBOL = 'MSFT'

db_data_feed = DBDataFeed()
# get all dates, where we have more than 99.98% of the data (more than 4670 points)
DATES_TO_ANALYSIS = db_data_feed.get_dates_for_symbol_min_data(SECURITY_SYMBOL, 4670)
# how many records to load
DATA_LIMIT = 10
data_loaded_from_db = []

dates_loaded = 0
for single_date in DATES_TO_ANALYSIS:
    print("Loading data for " + str(single_date))
    data = db_data_feed.get_prices_bars_for_day_for_symbol(single_date, SECURITY_SYMBOL)
    data_loaded_from_db.append((single_date, data))

    dates_loaded += 1
    if DATA_LIMIT > 0 and dates_loaded >= DATA_LIMIT:
        break

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

indicators_history_per_values = []

all_generated_values_count = len(generated_values)

for generated_value in generated_values:
    indicators_map = [
        # {'name': 'SMA_1', 'source': 'close',
        # 'implementation': SMA(generated_value['SMA_1']), 'passalldata': False},
        # {'name': 'SMA_2', 'source': 'close',
        # 'implementation': SMA(generated_value['SMA_2']), 'passalldata': False}
    ]

    perf_monitor = IndicatorsCalculatorPerfMonitor()
    indicators_history = {}
    for single_date, data in data_loaded_from_db:
        indicators_calculator = IndicatorsCalculator(performance_monitor=perf_monitor)
        # indicators_calculator.define_indicators_map(indicators_map)

        back_test_indicators_calculator = BacktestIndicatorsCalculator()
        indicators_history[single_date] = back_test_indicators_calculator.run_computation_for_data(data,
                                                                                                   indicators_calculator)

        print(single_date)

    for indicator_name, stats in perf_monitor.performance_stats:
        print(stats)
    all_generated_values_count -= 1
    print(f"Remaining data: {all_generated_values_count}")
