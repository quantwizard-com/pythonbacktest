from abc import abstractmethod, ABC
from typing import List

from pythonbacktest.ai.utils.indicatorshistorysource import IndicatorsHistorySource


class AbstractNode(ABC):

    def __init__(self, node_name):
        self.__node_name = node_name
        self.__indicators_history_source = None
        self.__node_result = None

    #@abstractmethod
    #def reset_node(self):
    #    raise NotImplementedError()

    @property
    def node_name(self):
        return self.__node_name

    @property
    def indicators_history_source(self) -> IndicatorsHistorySource:
        return self.__indicators_history_source

    def set_indicators_history_source(self, indicators_history_source: IndicatorsHistorySource):
        self.__indicators_history_source = indicators_history_source

    @property
    def current_node_result(self):
        return self.__node_result

    def set_node_result(self, result):
        self.__node_result = result

    def activate_node(self):
        self._activation_method()

    @abstractmethod
    def _activation_method(self):
        raise NotImplementedError()
