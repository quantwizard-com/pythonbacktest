from abc import abstractmethod


class AbstractDataFeed(object):
    def __init__(self):
        pass

    # get data for single day only
    # return price bars for the given date
    @abstractmethod
    def get_prices_bars_for_day(self, trading_day):
        raise Exception("Not implemented method!!!")

    # get data for single day only
    # return price bars for the given date for the given symbol
    @abstractmethod
    def get_prices_bars_for_day(self, trading_day, security_symbol):
        raise Exception("Not implemented method!!!")