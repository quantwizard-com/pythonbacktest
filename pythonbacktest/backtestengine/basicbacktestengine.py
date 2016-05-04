from . import *

from pythonbacktest.indicator import Indicators


class BasicBackTestEngine(AbstractBackTestEngine):

    def __init__(self, data_feed, strategy, broker):
        AbstractBackTestEngine.__init__(self, data_feed, strategy, broker)

    def start(self):

        for date, trading_day_data in self.data_feed.all_data.iteritems():
            self.__backtest_single_day(date, trading_day_data.price_bars)

    # run backtest on single day only
    def start_single_date(self, date):

        # let's extract single date and test price bars for that date
        price_bars_per_date = self.data_feed[date]

        if price_bars_per_date is None:
            raise "Can't extract data for date: " + date
        self.__backtest_single_day(date, price_bars_per_date)

    # backtest single date (as: single day) with give intraday price bars
    def __backtest_single_day(self, date, price_bars):

        indicators = Indicators()

        # allow strategy to set indicators from scratch for a new day
        self.strategy.init_indicators(indicators)

        for price_bar in price_bars:
            indicators.new_price_bar(price_bar)
            self.broker.set_current_price(price_bar.close)
            self.strategy.new_price_bar(price_bar, indicators)


