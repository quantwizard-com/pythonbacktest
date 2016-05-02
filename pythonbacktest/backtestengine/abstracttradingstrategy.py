import abc

from pythonbacktest import datafeed

class AbstractTradingStrategy(object):

    @abc.abstractmethod
    def new_price_bar(self, price_bar):
        raise NotImplementedError()
