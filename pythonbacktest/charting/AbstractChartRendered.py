import abc


class AbstractChartRendered(object):

    def __init__(self, width=900, height=500):
        self.__chart_width = width
        self.__chart_height = height

    # render indicators as a chart
    # indicators - indicators object, which could be addresses by names (implementation of Indicators)
    # markers - name of the indicators, which should act as markets on *all charts*
    # name_collections - collection(s) of tuples: (name of indicator, color);
    #                    if more than 1 collection is provided: multiple charts will be generated
    #                    with common x axis
    # sample usage:
    #  render_indicators(indicators, ['trade_sell', 'trade_buy'],
    #                   [('open', 'blue'), ('SMA100', 'green')], [('SMA10', 'yellow'), ('SMA20', 'red')])
    @abc.abstractmethod
    def render_indicators(self, indicators, markers, *name_collections):
        raise NotImplementedError()

    # render trades: buy, sell and short positions
    @abc.abstractmethod
    def render_trades(self, trade_log):
        raise NotImplementedError()

    @property
    def chart_width(self):
        return self.__chart_width

    @property
    def chart_height(self):
        return self.__chart_height
