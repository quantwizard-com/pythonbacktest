from pythonbacktest.indicatorshistory import IndicatorHistory


class IndicatorsHistoryIterator(object):
    """
    Class used to iterate through the IndicatorsHistory to feed data to the decisions network
    """
    def __init__(self, indicators_history: IndicatorHistory):
        self.__all_snapshots = list(indicators_history.all_snapshots.items())
        self.__current_timestamp_index = 0

    def move_to_next_snapshot(self) -> bool:
        self.__current_timestamp_index += 1

        return self.__current_timestamp_index < len(self.__all_snapshots)

    @property
    def current_snapshot(self) -> tuple:
        current_index = self.__current_timestamp_index
        if current_index < len(self.__all_snapshots):
            return self.__all_snapshots[current_index]
        else:
            raise ValueError('No more snapshots!')