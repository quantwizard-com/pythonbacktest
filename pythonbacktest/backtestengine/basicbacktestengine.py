from . import *

from pythonbacktest.indicator import Indicators


class BasicBackTestEngine(AbstractBackTestEngine):

    def __init__(self, data_feed, strategy, broker, indicator_history=None):
        AbstractBackTestEngine.__init__(self, data_feed, strategy, broker, indicator_history)

    def start(self):

        for date, trading_day_data in self.data_feed.all_data.iteritems():
            self.__backtest_single_day(date, trading_day_data.price_bars)

    # run backtest on single day only
    def start_single_date(self, date):

        # let's extract single date and test price bars for that date
        price_bars_per_date = self.data_feed.get_prices_bars_for_day(date)

        if price_bars_per_date is None:
            raise "Can't extract data for date: " + date
        self.__backtest_single_day(date, price_bars_per_date)

    # backtest single date (as: single day) with give intraday price bars
    def __backtest_single_day(self, date, price_bars):

        # create fresh set of indicators for each day
        indicators = Indicators()
        self.all_indicators_per_day[date] = indicators
        self.broker.set_indicators(indicators)

        # allow strategy to set indicators from scratch for a new day
        self.strategy.init_indicators(indicators)

        price_bar_index = 0
        for price_bar in price_bars:

            # this is point, where we trigger ALL non-transactional indicator calculation
            indicators.new_price_bar(price_bar)

            # this is transactional section - proceed only if broker AND strategy are set

            if self.broker and self.strategy:
                self.broker.set_current_price_bar(price_bar, price_bar_index)
                price_bar_index += 1

                # once everything's set, call the strategy to do the voodoo magic
                self.strategy.new_price_bar(price_bar, indicators, self.broker)

            # finally: preserve state of indicators in history (if needed)
            if self.indicator_history:
                self.indicator_history.record_state_of_indicators(price_bar.timestamp, indicators)


