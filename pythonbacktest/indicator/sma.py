# simple moving average calculation
from . import AbstractIndicator


class SMA(AbstractIndicator):

    def __init__(self, window_len):
        AbstractIndicator.__init__(self)

        self.__latest_result = None
        self.__window_len = window_len
        self.__data_storage = []

        # entire SMA data for all input which came
        self.__all_sma = []
        self.__sum_of_elements = 0

    def result(self):
        return self.__latest_result

    def all_result(self):
        return self.__all_sma

    def on_new_upstream_value(self, new_value):

        self.__sum_of_elements += new_value
        self.__data_storage.append(new_value)

        if len(self.__data_storage) == self.__window_len:

            # calculate current SMA value
            current_sma = self.__sum_of_elements * 1.0 / self.__window_len
            self.__latest_result = current_sma

            # reduce sum by the first element on the list
            # and remove that element from the data
            self.__sum_of_elements -= self.__data_storage[0]
            del self.__data_storage[0]

        self.__all_sma.append(self.__latest_result)