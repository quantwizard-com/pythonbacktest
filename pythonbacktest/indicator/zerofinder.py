from . import AbstractIndicator
import math


class ZeroFinder(AbstractIndicator):

    def __init__(self):
        AbstractIndicator.__init__(self)

        self.__all_input_values = []

        self.__all_distances = []

    @property
    def all_result(self):
        return self.__all_distances

    @property
    def result(self):
        return self.__all_distances[-1] if len(self.__all_distances) > 0 else None

    def on_new_upstream_value(self, new_value):
        if new_value is None:
            raise ValueError("None is not allowed")

        if type(new_value) is list:
            del self.__all_input_values[:len(new_value)]
            self.__all_input_values.extend(new_value)
        else:
            self.__all_input_values.append(new_value)

        self.__calculate_all_distances()

    def __calculate_all_distances(self):

        previous_value = None
        self.__all_distances = []

        for current_value in self.__all_input_values:
            current_distance_to_zero = None

            if previous_value is not None:
                current_distance_to_zero = self.__calculate_distance_to_zero(previous_value, current_value)

            self.__all_distances.append(current_distance_to_zero)

            previous_value = current_value

    def __calculate_distance_to_zero(self, previous_value, current_value):

        current_differential = current_value - previous_value

        # no change - return 0 if we're on 0, else: None
        if current_differential == 0:
            return 0 if current_value == 0 else None

        # above 0, still growing
        if current_value > 0 and current_differential > 0:
            return None

        # below 0, still falling
        if current_value < 0 and current_differential < 0:
            return None

        distance_to_zero = abs(current_value * 1.0 / current_differential)
        log_value = math.log(distance_to_zero + 1, 2)
        round_with_sign = -math.copysign(1, current_differential) * log_value

        return round_with_sign










