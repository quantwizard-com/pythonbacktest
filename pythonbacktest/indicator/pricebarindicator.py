from .base import AbstractIndicator
from pythonbacktest.datafeed import PriceBar


class PriceBarIndicator(AbstractIndicator):
    """
    Root of all other indicators; the only one which gets data injected directly
    """

    def __init__(self, indicator_name):
        AbstractIndicator.__init__(self,
                                   indicator_name=indicator_name,
                                   source_indicators=None)

        self.__current_pricebar = None

    def reset(self):
        AbstractIndicator.reset(self)

    def inject_new_price_bar(self, price_bar):
        if price_bar is None:
            raise ValueError("Price bar can't be None")

        if not isinstance(price_bar, PriceBar):
            raise ValueError("Passed data is not of PriceBar type")

        self.__current_pricebar = {
            "timestamp": price_bar.timestamp,
            "open": price_bar.open,
            "close": price_bar.close,
            "high": price_bar.high,
            "low": price_bar.low,
            "volume": price_bar.volume}

    def _process_new_upstream_record(self):
        if self.__current_pricebar is None:
            raise ValueError('Price bar record is not set')

        self.all_results.append(self.__current_pricebar)
        self.__current_pricebar = None


