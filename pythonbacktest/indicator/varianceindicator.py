from .base import AbstractIndicator
from numpy import var


class VAR(AbstractIndicator):

    def __init__(self, window_len):
        AbstractIndicator.__init__(self)
        self.__window_len = window_len
        self.reset()

    def reset(self):
        self.__latest_result = None
        self.__data_storage = []
        self.__all_var = []

    @property
    def result(self):
        return self.__latest_result

    @property
    def all_result(self):
        return self.__all_var

    def on_new_upstream_value(self, new_value):

        if new_value is None:
            self.__latest_result = None
            self.__all_var.append(None)
            return

        self.__data_storage.append(new_value)

        if len(self.__data_storage) == self.__window_len:

            # calculate current varience value
            current_var = var(self.__data_storage)
            self.__latest_result = current_var

            del self.__data_storage[0]

        self.__all_var.append(self.__latest_result)
