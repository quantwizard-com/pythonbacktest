# simple moving average calculation
from .base import AbstractIndicator


class SMA(AbstractIndicator):

    def __init__(self, indicator_name, window_len, source_indicators=None):
        super().__init__(indicator_name=indicator_name, source_indicators=source_indicators)

        self.__window_len = window_len
        self.reset()

    def reset(self):
        super().reset()
        self.__temp_data_storage = []
        self.__sum_of_elements = 0

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()

        if new_value is None:
            self.all_results.append(None)
            return

        self.__sum_of_elements += new_value
        self.__temp_data_storage.append(new_value)

        current_sma = None
        if len(self.__temp_data_storage) == self.__window_len:

            # calculate current SMA value
            current_sma = self.__sum_of_elements * 1.0 / self.__window_len

            # reduce sum by the first element on the list
            # and remove that element from the data
            self.__sum_of_elements -= self.__temp_data_storage[0]
            del self.__temp_data_storage[0]

        self.add_new_result(current_sma)
