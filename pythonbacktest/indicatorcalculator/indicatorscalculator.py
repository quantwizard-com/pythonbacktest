from typing import List

from pythonbacktest.indicatorshistory import IndicatorHistory
from pythonbacktest.datafeed import PriceBar
from .indicatorsmap import IndicatorsMap


class IndicatorsCalculator(object):

    def __init__(self, indicators_map: IndicatorsMap,
                    performance_monitor=None,
                 indicators_history: IndicatorHistory=None):

        self.__indicators_map = indicators_map
        self.__performance_monitor = performance_monitor
        self.__indicators_history = indicators_history

    def run_calculation(self, price_bars: List[PriceBar]):

        for single_price_bar in price_bars:

            self.__indicators_map.new_price_bar(single_price_bar)

            # update indicators history
            if self.__indicators_history:
                self.__indicators_history.take_map_snapshot(
                    single_price_bar.timestamp, self.__indicators_map)

