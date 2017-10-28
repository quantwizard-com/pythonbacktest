from abc import abstractmethod, ABC
from pythonbacktest.ai.utils.indicatorssource import IndicatorsSource


class AbstractNode(ABC):

    def __init__(self, indicators_source: IndicatorsSource):
        self.__indicators_source = indicators_source
        self.__node_result = None

    #@abstractmethod
    #def reset_node(self):
    #    raise NotImplementedError()

    @property
    def indicators_source(self) -> IndicatorsSource:
        return self.__indicators_source

    @property
    def current_node_result(self):
        return self.__node_result

    def set_node_result(self, result):
        self.__node_result = result

    def activate_node(self):
        self.__activation_method()

    @abstractmethod
    def _activation_method(self):
        raise NotImplementedError()
