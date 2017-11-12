from abc import abstractmethod, ABC

from pythonbacktest.indicatorshistory import AbstractSnapshot


class AbstractNode(ABC):

    def __init__(self, node_name):
        self.__node_name = node_name
        self.__indicators_history_source = None
        self.__node_result = None

    @property
    def node_name(self):
        return self.__node_name

    @property
    def current_node_result(self):
        return self.__node_result

    def set_node_result(self, result):
        self.__node_result = result

    def activate_node(self, indicators_snapshot: AbstractSnapshot):
        self._activation_method(indicators_snapshot)

    @abstractmethod
    def _activation_method(self, indicators_snapshot: AbstractSnapshot):
        raise NotImplementedError()
