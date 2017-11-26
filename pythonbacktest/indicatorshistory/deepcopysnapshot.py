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
        self.__all_snapshots_values_dict = {}
        self.__latest_snapshots_values_dict = {}

        super().__init__(indicators_map)

    def _take_snapshot(self, indicators_map: IndicatorsMap) -> Dict:

        referencial_length = -1

        for single_indicator in indicators_map.all_indicators():
            indicator_name = single_indicator.indicator_name
            indicator_all_results = single_indicator.all_results
            indicator_latest_result = single_indicator.latest_result

            if not indicator_all_results:
                raise ValueError(f"Indicator {indicator_name} returned null or empty all results.")

            # deep copy values of the given indicator
            self.__all_snapshots_values_dict[indicator_name] = list(indicator_all_results)
            self.__latest_snapshots_values_dict[indicator_name] = indicator_latest_result

            current_len = len(indicator_all_results)
            if referencial_length == -1:
                referencial_length = current_len
            elif referencial_length != current_len:
                raise ValueError(f"Expected of snapshot data len={referencial_length}, got {current_len}")

    @property
    def all_snapshot_values(self) -> Dict:
        return self.__all_snapshots_values_dict

    @property
    def latest_snapshot_values(self) -> Dict:
        return self.__latest_snapshots_values_dict
