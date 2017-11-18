from typing import Dict
from pythonbacktest.indicatorcalculator import IndicatorsMap
from pythonbacktest.indicatorshistory import AbstractSnapshot


class ReferencialSnapshot(AbstractSnapshot):
    """
    This snapshot will store only references to the latest results
    generated by the individual indicators. It won't be making actual copy
    of the data from those indicators.
    - Advantages: very fast, no copy operation involved
    - Disadvantages: can't be used if value of the indicator for the given timestamp will change
    """

    def __init__(self, indicators_map: IndicatorsMap):
        super().__init__(indicators_map)

    def _take_snapshot(self, indicators_map: IndicatorsMap) -> tuple:
        """
        Take snapshot of the values in the IndicatorsMap
        :param indicators_map: Map of the indicators
        :return: tuple (all snapshot values, latest snapshot values
        """
        all_snapshots_values_dict = {}
        latest_snapshots_values_dict = {}
        for single_indicator in indicators_map.all_indicators():
            indicator_name = single_indicator.indicator_name
            all_snapshots_values_dict[indicator_name] = single_indicator.all_results
            latest_snapshots_values_dict[indicator_name] = single_indicator.latest_result

        return all_snapshots_values_dict, latest_snapshots_values_dict



