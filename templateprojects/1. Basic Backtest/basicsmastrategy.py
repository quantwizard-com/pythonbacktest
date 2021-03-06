from pythonbacktest.strategy import AbstractTradingStrategy
from pythonbacktest.indicator import SMA


class BasicSMAStrategy(AbstractTradingStrategy):

    def __init__(self):
        AbstractTradingStrategy.__init__(self)

    def init_indicators(self, indicators):
        indicators.define_indicators_map(
            [
                {'name': 'SMA200', 'source': 'close', 'implementation': SMA(200)},
                {'name': 'SMA50', 'source': 'close', 'implementation': SMA(50)}
            ])

    def new_price_bar(self, price_bar, indicators, broker):
        current_SMA200 = indicators['SMA200']
        current_SMA50 = indicators['SMA50']
        current_position = broker.current_position

        if current_SMA50 is not None and current_SMA200 is not None:
            if current_position <= 0:
                if current_SMA50 > current_SMA200:
                    broker.go_long(100)

            if current_position > 0:
                if current_SMA50 < current_SMA200:
                    broker.go_sell(100)

    def day_end(self, final_price_bar, indicators, broker):
        broker.cover_position()
