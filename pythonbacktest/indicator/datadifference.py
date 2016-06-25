from . import *
import itertools


class DataDifference(AbstractIndicator):

    def __init__(self):
        self.__input_data_1 = []
        self.__input_data_2 = []
        self.__output_data = []

    @property
    def result(self):
        return None if not self.__output_data else self.__output_data[-1]

    @property
    def all_result(self):
        return self.__output_data

    def on_new_upstream_value(self, *new_value):

        if len(new_value) != 2:
            raise ValueError("Expected 2 parameters")

        passed_param_1 = new_value[0]
        passed_param_2 = new_value[1]

        if type(passed_param_1) is list:
            len_param_1 = len(passed_param_1)
            len_param_2 = len(passed_param_2)

            if len_param_1 == len_param_2:
                del self.__input_data_1[:len_param_1]
                self.__input_data_1.extend(passed_param_1)

                del self.__input_data_2[:len_param_2]
                self.__input_data_2.extend(passed_param_2)

                self.__recalculate_differences()
            else:
                raise ValueError("Passed parameters must have the same length")
        else:
            self.__input_data_1.append(passed_param_1)
            self.__input_data_2.append(passed_param_2)
            result = passed_param_1 - passed_param_2 if passed_param_1 is not None and passed_param_2 is not None else None
            self.__output_data.append(result)


    def __recalculate_differences(self):
        self.__output_data = []

        for param1, param2 in itertools.izip(self.__input_data_1, self.__input_data_2):
            self.__output_data.append(param1 - param2)


