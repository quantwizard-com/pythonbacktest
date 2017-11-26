from abc import ABC, abstractmethod
from typing import Dict, Text

from pythonbacktest.indicatorcalculator import IndicatorsMap


class AbstractSnapshot(ABC):

    def __init__(self, indicators_map: IndicatorsMap):
        self._take_snapshot(indicators_map=indicators_map)

    @abstractmethod
    def _take_snapshot(self, indicators_map: IndicatorsMap) -> tuple:
        """
        Take snapshot of the values in the IndicatorsMap
        :param indicators_map: Map of the indicators
        :return: tuple (all snapshot values, latest snapshot values)
        """
        raise NotImplementedError()

    @property
    def all_snapshot_values(self) -> Dict:
        raise NotImplementedError()

    @property
    def latest_snapshot_values(self) -> Dict:
        raise NotImplementedError()

    @property
    def get_current_indicator_value(self, indicator_name):
        return self.latest_snapshot_values[indicator_name]

    @property
    def __getitem__(self, indicator_name: Text):
        return self.get_current_indicator_value(indicator_name)