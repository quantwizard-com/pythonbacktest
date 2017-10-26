# moving standard deviation
from .base import AbstractIndicator
from numpy import std


class STD(AbstractIndicator):

    def __init__(self, window_len):
        AbstractIndicator.__init__(self)
        self.__window_len = window_len
        self.reset()

    def reset(self):
        self.__latest_result = None
        self.__data_storage = []
        self.__all_std = []

    @property
    def result(self):
        return self.__latest_result

    @property
    def all_result(self):
        return self.__all_std

    def on_new_upstream_value(self, new_value):

        if new_value is None:
            self.__latest_result = None
            self.__all_std.append(None)
            return

        self.__data_storage.append(new_value)

        if len(self.__data_storage) == self.__window_len:

            # calculate current standard deviation value
            current_std = std(self.__data_storage)
            self.__latest_result = current_std

            del self.__data_storage[0]

        self.__all_std.append(self.__latest_result)
