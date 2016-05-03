from . import *


class BasicBackTestEngine(AbstractBackTestEngine):

    def __init__(self, data_feed, strategy):
        AbstractBackTestEngine.__init__(self, data_feed, strategy)

    def start(self):

        for date, price_bars in self.data_feed.get_prices_bars_for_day():
            self.__backtest_single_day(date, price_bars)

    # run backtest on single day only
    def start_single_date(self, date):

        # let's extract single date and test price bars for that date
        price_bars_per_date = self.data_feed[date]

        if price_bars_per_date is None:
            raise "Can't extract data for date: " + date
        self.__backtest_single_day(date, price_bars_per_date)

    # backtest single date (as: single day) with give intraday price bars
    def __backtest_single_day(self, date, price_bars):
        for price_bar in price_bars:
            self.strategy(price_bar)


