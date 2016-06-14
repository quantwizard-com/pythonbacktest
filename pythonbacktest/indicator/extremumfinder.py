from . import AbstractIndicator


# this class is responsible for estimating distance to the next extremum (minimum or maximum)
# on the x axis
class ExtremumFinder(AbstractIndicator):

    def __init__(self):
        AbstractIndicator.__init__(self)

        self.__all_input_values = []

        self.__all_distances = []

    @property
    def result(self):
        return self.__all_distances[-1] if len(self.__all_distances) > 0 else None

    @property
    def all_result(self):
        return self.__all_distances

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

        previous_differential_l1 = None
        previous_value = None

        for current_value in self.__all_input_values:
            current_distance = None

            if previous_value is not None:
                current_differential = current_value - previous_value

                if previous_differential_l1 is not None:
                    current_distance = self.__calculate_distance_to_extremum(previous_differential_l1, current_differential)

                previous_differential_l1 = current_differential

            previous_value = current_value
            self.__all_distances.append(current_distance)

    def __calculate_distance_to_extremum(self, previous_differential_l1, current_differential_l1):

        current_differential_l2 = current_differential_l1 - previous_differential_l1

        # we need to calculate when differential will hit 0
        if current_differential_l1 == 0:
            return 0

        # constant growth, above 0
        if current_differential_l1 > 0 and current_differential_l2 > 0:
            return None

        # constant fall, below 0
        if current_differential_l1 < 0 and current_differential_l2 < 0:
            return None

        # constant differential (== zero on L2 differential)
        if current_differential_l2 == 0:
            return None

        current_distance = abs(current_differential_l1 * 1.0 / current_differential_l2)

        return current_distance


