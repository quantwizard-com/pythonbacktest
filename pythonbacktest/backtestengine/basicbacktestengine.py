from pythonbacktest import backtestengine


class BasicBackTestEngine(backtestengine.AbstractBackTestEngine):

    def __init__(self, data_feed, strategy):
        backtestengine.AbstractBackTestEngine.__init__(self, data_feed, strategy)

    def start(self):
        raise NotImplementedError()

    # run backtest on single day only
    def start_single_date(self, date):
        pass

    def __backtest_single_day(self, date, price_bars):
        pass


