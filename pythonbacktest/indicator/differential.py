from . import AbstractIndicator


class Differential(AbstractIndicator):

    def __init__(self):
        AbstractIndicator.__init__(self)

        self.__last_value = None

        # entire SMA data for all input which came
        self.__all_differential = []

        # all values passed to this indicator
        self.__all_values = []

    @property
    def result(self):
        return self.__all_differential[-1]

    @property
    def all_result(self):
        return self.__all_differential

    def on_new_upstream_value(self, new_value):

        # we expect None or array of numbers, which has exactly 'window_size' elements
        if new_value is None:
            self.__all_values.append(None)
        else:
            if type(new_value) is list:
                del self.__all_values[:len(new_value)]
                self.__all_values.extend(new_value)

                # ... and recalculate entire differential
                self.__recalculate_all_diff()
            else:
                self.__all_values.append(new_value)
                self.__recalculate_all_diff()

    def __recalculate_all_diff(self):
        self.__all_differential = []

        last_value = None
        diff = None
        for value in self.__all_values:

            if last_value is not None:
                diff = value - last_value

            self.__all_differential.append(diff)
            last_value = value

        self.__last_value = last_value





