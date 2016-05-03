from pythonbacktest.strategy import AbstractTradingStrategy
from pythonbacktest.indicator import SMA


class BasicSMAStrategy(AbstractTradingStrategy):

    def init_indicators(self, indicators):
        indicators.set_indicators(
            [
                ('SMA200', 'close', SMA(200))
            ])

    def new_price_bar(self, price_bar, indicators):
        print indicators['close']
