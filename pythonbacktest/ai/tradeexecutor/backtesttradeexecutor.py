from pythonbacktest.datafeed import PriceBar
from .abstracttradeexecutor import AbstractTradeExecutor


class BackTestTradeExecutor(AbstractTradeExecutor):

    def __init__(self):
        super().__init__()
        self.__current_price_bar = None

    def set_current_price_bar(self, price_bar: PriceBar):
        self.__current_price_bar = price_bar

    def sell(self):
        pass

    def buy(self):
        pass

    def ssell(self):
        pass