class AbstractDataFeed(object):

    def __init__(self):

        # data feed data storage - dictionary
        # key - date of the data
        # value - collection of TradingDayData ordered by date for the given day
        self.__data = {}

        self.__data_view_range = (0, None)

    @property
    def all_data(self):
        return self.__data

    def set_data_view_range(self, min_index = 0, max_index = None):
        self.__data_view_range = (min_index, max_index)

    # get data for single day only
    # return price bars for the given date
    def get_prices_bars_for_day(self, trading_day):

        if self.__data_view_range[1] is None:
            return self.__data[trading_day].price_bars[self.__data_view_range[0]:]
        else:
            return self.__data[trading_day].price_bars[self.__data_view_range[0]:self.__data_view_range[1] + 1]
