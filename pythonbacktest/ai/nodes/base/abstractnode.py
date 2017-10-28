from abc import abstractmethod, ABC

from pythonbacktest.indicatorcalculator import IndicatorsMap
from pythonbacktest.indicatorshistory import AbstractSnapshot

class AbstractNode(ABC):

    def __init__(self, indicators_map: IndicatorsMap):
        self.__indicators_map = indicators_map

    @abstractmethod
    def reset_node(self):
        raise NotImplementedError()

    @property
    def current_value(self):
        raise NotImplementedError()

    @property
    def all_collected_values(self):
        raise NotImplementedError()
