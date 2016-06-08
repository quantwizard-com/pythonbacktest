class AbstractDataFeed(object):

    def __init__(self):

        # data feed data storage - dictionary
        # key - date of the data
        # value - collection of TradingDayData ordered by date for the given day
        self.__data = {}

    @property
    def all_data(self):
        return self.__data

    # get data for single day only
    # return price bars for the given date
    def get_prices_bars_for_day(self, trading_day):
        return self.__data[trading_day].price_bars
