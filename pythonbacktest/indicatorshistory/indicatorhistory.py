from collections import OrderedDict

from pythonbacktest.indicatorcalculator.indicatorsmap import IndicatorsMap


class IndicatorHistory(object):

    def __init__(self, snapshot_type):
        self.__snapshot_type = snapshot_type

        # snapshots history records:
        # - key - timestamp
        # - value - indicators snapshot
        self.__history_records = OrderedDict()

    def take_map_snapshot(self, timestamp, indicators_map: IndicatorsMap):
        snapshot_object = self.__snapshot_type(indicators_map)

        self.__history_records[timestamp] = snapshot_object

    @property
    def all_history(self):
        return self.__history_records

    @property
    def all_snapshots(self):
        return self.all_history

    @property
    def last_snapshot(self):
        """
        Take last snapshot saved in the history
        :return:
        """
        # lets get last record
        last_index = next(reversed(self.__history_records.keys()))
        last_value = self.__history_records[last_index]
        return last_index, last_value

