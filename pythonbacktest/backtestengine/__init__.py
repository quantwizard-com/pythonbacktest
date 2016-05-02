"""
.. moduleauthor:: Krzysztof Wasiak (k.wasiak@gmail.com)
"""
import abc

from pythonbacktest import broker


class AbstractBackTestEngine(object):

    def __init__(self, data_feed, strategy):
        self.__data_feed = data_feed
        self.__strategy = strategy
        self.__broker = broker.BackTestBroker()

    # start back test procedure
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def start_single_date(self, date):
        raise NotImplemented()

