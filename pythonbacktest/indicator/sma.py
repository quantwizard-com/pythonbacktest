# simple moving average calculation
from . import AbstractIndicator


class SMA(AbstractIndicator):

    def __init__(self, window_len, source_indicators):
        if len(source_indicators) != 1:
            raise ValueError("Expecting 1 source indicator only")

        AbstractIndicator.__init__(self, source_indicators=source_indicators)

        self.__window_len = window_len
        self.reset()

    def reset(self):
        AbstractIndicator.reset(self)
        self.__temp_data_storage = []
        self.__sum_of_elements = 0

    def __process_new_upstream_record(self):
        new_value = self.source_indicators[0].latest_result

        if new_value is None:
            self.__latest_result = None
            self.all_results.append(None)
            return

        self.__sum_of_elements += new_value
        self.__temp_data_storage.append(new_value)

        if len(self.__temp_data_storage) == self.__window_len:

            # calculate current SMA value
            current_sma = self.__sum_of_elements * 1.0 / self.__window_len
            self.__latest_result = current_sma

            # reduce sum by the first element on the list
            # and remove that element from the data
            self.__sum_of_elements -= self.__temp_data_storage[0]
            del self.__temp_data_storage[0]

        self.all_results.append(self.__latest_result)
