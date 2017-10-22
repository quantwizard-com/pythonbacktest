from pythonbacktest.datafeed import DBDataFeed
from pythonbacktest.indicator import SMA

from pythonbacktest.indicatorcalculator import IndicatorsMap

import random

indicators_map_definition = [
    {'sources': 'open', 'implementation': SMA(indicator_name='SMA', window_len=50)}
]

indicators_map = IndicatorsMap(indicators_map_definition=indicators_map_definition)

SECURITY_SYMBOL = 'MSFT'

db_data_feed = DBDataFeed()
DATES_TO_ANALYSIS = db_data_feed.get_dates_for_symbol_min_data(SECURITY_SYMBOL, 4670)

# get data for the random date
single_date = random.choice(DATES_TO_ANALYSIS)
data = db_data_feed.get_prices_bars_for_day_for_symbol(single_date, SECURITY_SYMBOL)

