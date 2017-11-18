from typing import Dict
from pythonbacktest.indicatorcalculator import IndicatorsMap
from pythonbacktest.indicatorshistory import AbstractSnapshot


class DeepCopySnapshot(AbstractSnapshot):
    """
    This snapshot will store deep copy of the indicators results
    generated by the individual indicators.
    - Advantages: very accurate result for indicators changing over time (i.e.: which can have multiple values
           for the same timestamp over time
    - Disadvantages: very slow, should be used only in cases of the dynamically changing indicator results
    """

    def __init__(self, indicators_map: IndicatorsMap):
        super().__init__(indicators_map)

    def _take_snapshot(self, indicators_map: IndicatorsMap) -> Dict:

        snapshot_dict = {}
        for single_indicator in indicators_map.all_indicators():
            indicator_name = single_indicator.indicator_name
            snapshot_dict[indicator_name] = list(single_indicator.all_results)

        return snapshot_dict