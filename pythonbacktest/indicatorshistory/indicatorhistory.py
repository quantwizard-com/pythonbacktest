from collections import OrderedDict

from pythonbacktest.indicatorcalculator.indicatorsmap import IndicatorsMap


class IndicatorHistory(object):

    def __init__(self, snapshot_type):
        self.__snapshot_type = snapshot_type

        # snapshots history records:
        # - key - timestamp
        # - value - indicators snapshot
        self.__indicator_snapshot_records = OrderedDict()

    def take_map_snapshot(self, timestamp, indicators_map: IndicatorsMap):
        snapshot_object = self.__snapshot_type(indicators_map)

        self.__indicator_snapshot_records[timestamp] = snapshot_object

    @property
    def all_snapshots_per_indicator_names(self):
        return self.__indicator_snapshot_records

    @property
    def last_snapshot_per_indicator_names_per_day(self):
        """
        Take last snapshot saved in the history
        :return: Tuple: (timestamp, snapshot data)
        """
        # lets get last record per dat (index = timestamp)
        last_timestamp = next(reversed(self.__indicator_snapshot_records.keys()))
        last_snapshot_data_per_day = self.__indicator_snapshot_records[last_timestamp]
        return last_timestamp, last_snapshot_data_per_day

