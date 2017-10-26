from .base import AbstractIndicator


class Differential(AbstractIndicator):

    def __init__(self):
        AbstractIndicator.__init__(self)

        self.reset()

    def reset(self):
        self.__last_value = None
        self.__all_differential = []
        self.__all_values = []

    @property
    def result(self):
        return self.__all_differential[-1]

    @property
    def all_result(self):
        return self.__all_differential

    def on_new_upstream_value(self, new_value):

        # we expect None or array of numbers, which has exactly 'window_size' elements
        if type(new_value) is list:
            del self.__all_values[:len(new_value)]
            self.__all_values.extend(new_value)
            # ... and recalculate entire differential
            self.__recalculate_all_diff()
        else:
            self.__all_values.append(new_value)
            self.__calculate_last_diff()

    def __recalculate_all_diff(self):
        self.__all_differential = []

        last_value = None
        for value in self.__all_values:
            diff = self.__calculate_diff(last_value, value)
            self.__all_differential.append(diff)
            last_value = value
        self.__last_value = last_value

    def __calculate_last_diff(self):
        diff = None
        if len(self.__all_values) > 1:
            diff = self.__calculate_diff(self.__all_values[-2], self.__all_values[-1])
        self.__all_differential.append(diff)


    @staticmethod
    def __calculate_diff(previous_value, next_value):
        diff = None
        if previous_value is not None and next_value is not None:
            diff = next_value - previous_value

        return diff





