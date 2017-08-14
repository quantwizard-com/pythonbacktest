from . import AbstractIndicator
import decimal

class TrendTracker(AbstractIndicator):
    def __init__(self):
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
        self.__all_results = self.__recalculate_single_serie_result()

    def __recalculate_single_serie_result(self):

        previous_numerical_record = None
        previous_numerical_record_index = None
        local_minimum = None
        local_maximum = None
        looking_for_minimum = None
        looking_for_maximum = None
        first_record = True
        current_index = 0

        all_results = []

        for single_record in self.__all_input_data:
            if single_record is not None:
                if previous_numerical_record is not None:
                    if single_record > previous_numerical_record:
                        if looking_for_minimum:
                            #we've hit a local minimum
                            all_results[previous_numerical_record_index] = (previous_numerical_record, None)

                            looking_for_maximum = True
                            looking_for_minimum = False

                        if looking_for_maximum is None:
                            looking_for_maximum = True

                    if single_record < previous_numerical_record:
                        if looking_for_maximum:
                            #we've hit a local maximum
                            all_results[previous_numerical_record_index] = (None, previous_numerical_record)

                            looking_for_maximum = False
                            looking_for_minimum = True

                        if looking_for_minimum is None:
                            looking_for_minimum = True

                previous_numerical_record = single_record
                previous_numerical_record_index = current_index

            all_results.append((None, None))

            current_index += 1

        return all_results
