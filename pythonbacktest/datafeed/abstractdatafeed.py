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
        return self.__data[trading_day].get_price_bars

    # return iterator, which moves via individual trading days
    # return: iterator over tuple: (date, price bars)
    def trading_days_iterator(self):
        for date, trading_day_data in self.__data:
            yield date, trading_day_data.get_price_bars
