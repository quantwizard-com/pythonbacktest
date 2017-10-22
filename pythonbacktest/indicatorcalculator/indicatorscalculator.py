from pythonbacktest.indicatorcalculator import IndicatorsSnapshot
from pythonbacktest.indicator.staticvalue import StaticValue
from collections import OrderedDict
import time


class IndicatorsCalculator(object):

    def __init__(self, indicators_map, performance_monitor=None, snapshot_store=None):
        # counter which checks how many price bars in total have been processed at the indicators
        # number of processed bars should be consistent with number of results per each indicator
        # so this counter is used primarily to check on how individual indicators behave
        self.__price_bars_counter = 0

        self.__indicators_map = indicators_map
        self.__performance_monitor = performance_monitor
        self.__snapshot_store = snapshot_store

    def run_calculation(self, input_data):
        pass
