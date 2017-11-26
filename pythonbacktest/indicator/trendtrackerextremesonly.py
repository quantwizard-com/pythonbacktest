from .base import AbstractIndicator


class TrendTrackerExtremesOnly(AbstractIndicator):

    def __init__(self, indicator_name, level=1, source_indicators=None):
        AbstractIndicator.__init__(self,
                                   indicator_name=indicator_name,
                                   source_indicators=source_indicators)

        self.__level = level
        self.reset()

    def reset(self):
        AbstractIndicator.reset(self)
        self.__all_input_data = []

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()

        self.__all_input_data.append(new_value)
        self.__recalculate_all_result()

    def __recalculate_all_result(self):

        support_data = self.__all_input_data
        resistance_data = self.__all_input_data
        current_level = self.__level

        while current_level > 0:
            resistance_data = self.__calculate_resistance(resistance_data)
            support_data = self.__calculate_support(support_data)

            current_level -= 1

        AbstractIndicator.set_all_results(self, self.__flat_to_extremes_only(support_data, resistance_data))

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