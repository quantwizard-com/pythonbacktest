import copy

from pythonbacktest.indicator import PriceBarIndicator
from pythonbacktest.datafeed import PriceBar
from pythonbacktest.indicator.base import AbstractIndicator


class AggregatedPriceBar(AbstractIndicator):
    """
    This is PriceBar (open, high, low, close, volume) aggregated over multiple pricebars
    """
    def __init__(self, indicator_name, no_to_aggregate=0, source_indicators=None):
        """
        Constructor
        :param indicator_name: Name of the indicator
        :param no_to_aggregate: Number of input pricebars to aggregate before generating a new one
        :param source_indicators: Source indicator. MUST BE a PriceBar instance
        """
        super().__init__(indicator_name, source_indicators)

        if not isinstance(source_indicators, PriceBarIndicator):
            raise ValueError('Expected single instance of PriceBarIndicator, got instead: ' + str(type(source_indicators)))

        self.__no_to_aggregate = no_to_aggregate
        self.__previous_aggregated_price_bar = None
        self.__aggregated_price_bars = 0

    def reset(self):
        super().reset()

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()

        if new_value is None:
            self.all_results.append(None)
            return

        if self.__previous_aggregated_price_bar is None or \
                (self.__no_to_aggregate == self.__aggregated_price_bars and self.__no_to_aggregate > 0):

            self.__previous_aggregated_price_bar = PriceBar(dict_fields=new_value)
            self.all_results.append(self.__previous_aggregated_price_bar)
            self.__aggregated_price_bars = 1
            return

        aggregated_price_bar = self.__calculate_aggregated_price_bar(new_value)
        self.all_results.append(aggregated_price_bar)
        self.__aggregated_price_bars += 1
        self.__previous_aggregated_price_bar = aggregated_price_bar

    def __calculate_aggregated_price_bar(self, new_price_bar: PriceBar):
        result = copy.deepcopy(self.__previous_aggregated_price_bar)
        result.close = new_price_bar['close']
        result.high = max(result.high, new_price_bar['high'])
        result.low = min(result.low, new_price_bar['low'])
        result.volume += new_price_bar['volume']

        return result


