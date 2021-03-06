from . import AbstractIndicator
import decimal

class TrendTrackerExtremesOnly(AbstractIndicator):
    def __init__(self, level=1):
        self.__level = level
        self.reset()

    def reset(self):
        self.__all_results = []
        self.__all_input_data = []

    def on_new_upstream_value(self, new_value):
        if type(new_value) is list:
            del self.__all_input_data[:len(new_value)]
            self.__all_input_data.extend(new_value)
        else:
            self.__all_input_data.append(new_value)

        self.__recalculate_all_result()

    @property
    def result(self):
        pass

    @property
    def all_result(self):
        return self.__all_results

    def __recalculate_all_result(self):

        support_data = self.__all_input_data
        resistance_data = self.__all_input_data
        current_level = self.__level

        while current_level > 0:
            resistance_data = self.__calculate_resistance(resistance_data)
            support_data = self.__calculate_support(support_data)

            current_level -= 1

        self.__all_results = self.__flat_to_extremes_only(support_data, resistance_data)

    def __flat_to_extremes_only(self, support_data, resistance_data):
        data_to_process = zip(support_data, resistance_data)
        return [s if s else r for (s, r) in data_to_process]

    def __calculate_support(self, input_data):
        previous_numerical_record = None
        previous_numerical_record_index = None
        looking_for_minimum = None
        current_index = 0

        all_results = []

        for single_record in input_data:
            if single_record is not None:
                if previous_numerical_record is not None:
                    if single_record > previous_numerical_record:
                        if looking_for_minimum:
                            #we've hit a local minimum
                            all_results[previous_numerical_record_index] = previous_numerical_record
                            looking_for_minimum = False

                    if single_record < previous_numerical_record:
                        if not looking_for_minimum:
                            looking_for_minimum = True

                previous_numerical_record = single_record
                previous_numerical_record_index = current_index

            all_results.append(None)
            current_index += 1
        return all_results

    def __calculate_resistance(self, input_data):
        previous_numerical_record = None
        previous_numerical_record_index = None
        looking_for_maximum = None
        current_index = 0

        all_results = []

        for single_record in input_data:
            if single_record is not None:
                if previous_numerical_record is not None:
                    if single_record > previous_numerical_record:
                        if not looking_for_maximum:
                            looking_for_maximum = True

                    if single_record < previous_numerical_record:
                        if looking_for_maximum:
                            #we've hit a local maximum
                            all_results[previous_numerical_record_index] = previous_numerical_record

                            looking_for_maximum = False

                previous_numerical_record = single_record
                previous_numerical_record_index = current_index

            all_results.append(None)
            current_index += 1
        return all_results