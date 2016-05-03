import abc

from pythonbacktest import datafeed

class AbstractTradingStrategy(object):

    # set all the indicators, which need to be calculated for this strategy
    # argument: indicators - instance of the Indicators class
    @abc.abstractmethod
    def init_indicators(self, indicators):
        raise NotImplementedError()

    @abc.abstractmethod
    def new_price_bar(self, price_bar, indicators):
        raise NotImplementedError()
