from typing import List

from pythonbacktest.datafeed import PriceBar
from pythonbacktest.indicatorcalculator import IndicatorsSnapshot
from pythonbacktest.indicator.staticvalue import StaticValue
from .indicatorsmap import IndicatorsMap
from collections import OrderedDict
import time


class IndicatorsCalculator(object):

    def __init__(self, indicators_map: IndicatorsMap, performance_monitor=None, snapshot_store=None):
        self.__indicators_map = indicators_map
        self.__performance_monitor = performance_monitor
        self.__snapshot_store = snapshot_store

    def run_calculation(self, price_bars: List[PriceBar]):
        for single_price_bar in price_bars:
            self.__indicators_map.new_price_bar(single_price_bar)
