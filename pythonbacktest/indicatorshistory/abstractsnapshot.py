from abc import ABC, abstractmethod
from typing import Dict

from pythonbacktest.indicatorcalculator import IndicatorsMap


class AbstractSnapshot(ABC):

    def __init__(self, indicators_map: IndicatorsMap):
        self.__snapshot_values = self._take_snapshot(indicators_map=indicators_map)

    @abstractmethod
    def _take_snapshot(self, indicators_map: IndicatorsMap):
        """
        Take snapshot of the values in the IndicatorsMap
        :param indicators_map: Map of the indicators
        :return:
        """
        raise NotImplementedError()

    def snapshot_values(self) -> Dict:
        return self.__snapshot_values


