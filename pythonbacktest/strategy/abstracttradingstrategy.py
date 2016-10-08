import abc

from pythonbacktest import datafeed

class AbstractTradingStrategy(object):

    @abc.abstractmethod
    def new_price_bar(self, price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker):
        """
        New price bar just arrived
        :param price_bar: Price bar structure (timestamp, open, close, high, low, volume)
        :param indicators_snapshot: Snapshot of all indicator values up to this point in time (i.e.: timestamp)
        :param latest_indicators_values: Value of the indicator values at exactly point in time (i.e.: timestamp)
        :param broker: Broker, which will collect orders
        :return:
        """
        raise NotImplementedError()

    # event fired when we hit the last price bar
    @abc.abstractmethod
    def day_end_price_bar(self, price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker):
        raise NotImplementedError()
