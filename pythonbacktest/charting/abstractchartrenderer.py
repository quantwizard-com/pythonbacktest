import abc

from pythonbacktest.visualization import AbstractDataVisualization


class AbstractChartRenderer(AbstractDataVisualization):

    def __init__(self, width=900, height=500):
        AbstractDataVisualization.__init__(self)

        self.__chart_width = width
        self.__chart_height = height

    @abc.abstractmethod
    def render_charts(self, date_to_display):
        raise NotImplementedError()

    @property
    def chart_width(self):
        return self.__chart_width

    @property
    def chart_height(self):
        return self.__chart_height


