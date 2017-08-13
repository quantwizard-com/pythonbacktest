from . import AbstractIndicator
import decimal

class TrendTracker(AbstractIndicator):
    def __init__(self):
        self.reset()

    def reset(self):
        self.__all_results = []
        self.__all_input_data = []

    def on_new_upstream_value(self, new_value):
        self.__all_input_data.append(new_value)

    @property
    def result(self):
        pass

    @property
    def all_result(self):
        pass

    def __recalculate_result(self, looking_for_support):
        self.reset()

        looking_for_resistance = not looking_for_support
        baseline = -1.0
        current_index = 0
        reference_index = 0
        reference_angle = 999999999.99 if looking_for_support else -999999999.99
        results = []

        for input_number in self.__all_input_data:
            if input_number is not None:

                if baseline == -1.0:
                    baseline = input_number
                else:
                    current_angle = (input_number - baseline) / current_index

                    if looking_for_support and current_angle <= reference_angle:
                        reference_angle = current_angle
                    elif looking_for_resistance and current_angle >= reference_angle:
                        reference_angle = current_angle

            else:
                self.__all_results.append(None)

            current_index += 1
