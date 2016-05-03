from pythonbacktest.strategy import AbstractTradingStrategy


class BasicSMAStrategy(AbstractTradingStrategy):

    def init(self, indicators):
        indicators.set_indicators(
            [sma(input="close", name="SMA100", window=100),
             sma(input="SMA100", name="SMASMA100", window=100)]
        )

    def new_price_bar(self, price_bar):
        pass