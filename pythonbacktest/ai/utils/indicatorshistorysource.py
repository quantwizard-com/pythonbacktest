from pythonbacktest.indicatorshistory import IndicatorHistory
from .indicatorshistoryiterator import IndicatorsHistoryIterator


class IndicatorsHistorySource(object):

    def __init__(self, indicators_history: IndicatorHistory):
        self.__indicators_history_iterator = IndicatorsHistoryIterator(indicators_history)
        self.__current_timestamp, self.__snapshot = self.__indicators_history_iterator.current_snapshot()

    def move_to_next_timestamp(self) -> bool:
        """
        Move to next timestamp. Return false if there's no more timestamps
        :return: False - no more timestamps
        """
        if self.__indicators_history_iterator.move_to_next_snapshot():
            self.__current_timestamp, self.__snapshot = self.__indicators_history_iterator.current_snapshot()
            return True

        return False

    def get_current_indicator_value(self, indicator_name):
        return self.__snapshot.get_current_indicator_value(indicator_name)

    def __getitem__(self, indicator_name):
        return self.get_current_indicator_value(indicator_name)