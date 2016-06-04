from . import AbstractIndicator


# tracker for dynamic indicators
# it's purpose is tracking mix and max values of upstream indicators at the given time slot
# for static indicators: min and max will have the same value all the time
# (the value at the given time won't change)
class MinMaxTracker(AbstractIndicator):

    def __init__(self):

        # collection with (min, max) tupples
        self.__all_min_max = []

    @property
    def result(self):
        return self.__all_min_max[-1]

    @property
    def all_result(self):
        return self.__all_min_max

    def on_new_upstream_value(self, new_value):

        if new_value is None:
            self.__all_min_max.append(None)
        else:
            if type(new_value) is list:

                self.__update_result(new_value)

            else:
                raise ValueError("Non-list types are not supported.")

    def __update_result(self, input_list):

        current_result_index = 0
        for input_item in input_list:
            if len(self.__all_min_max) > current_result_index:
                current_result = self.__all_min_max[current_result_index]
                current_min = min(current_result[0], input_item)
                current_max = max(current_result[1], input_item)
                self.__all_min_max[current_result_index] = (current_min, current_max)
            else:
                self.__all_min_max.append((input_item, input_item))

            current_result_index += 1
