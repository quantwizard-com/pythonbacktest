import abc

from pythonbacktest import broker


class AbstractBackTestEngine(object):

    def __init__(self, data_feed, strategy, broker):
        self.__data_feed = data_feed
        self.__strategy = strategy
        self.__broker = broker

        # list of indicators collected per day for the current security
        # format:
        # key - date (day)
        # value - indicators
        self.__all_indicators_per_day = {}

    @property
    def data_feed(self):
        return self.__data_feed

    @property
    def strategy(self):
        return self.__strategy

    @property
    def broker(self):
        return self.__broker

    # start back test procedure
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def start_single_date(self, date):
        raise NotImplemented()

    @property
    def all_indicators_per_day(self):
        return self.__all_indicators_per_day
