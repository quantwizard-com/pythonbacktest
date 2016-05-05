# simple moving average calculation
from . import AbstractIndicator


class Differential(AbstractIndicator):

    def __init__(self):
        AbstractIndicator.__init__(self)

        self.__latest_result = None
        self.__last_value = None

        # entire SMA data for all input which came
        self.__all_differential = []

    @property
    def result(self):
        return self.__latest_result

    @property
    def all_result(self):
        return self.__all_differential

    def on_new_upstream_value(self, new_value):

        difference = None

        if self.__last_value is not None:
            difference = new_value - self.__latest_result

        self.__all_differential.append(difference)
        self.__latest_result = difference
        self.__last_value = new_value
