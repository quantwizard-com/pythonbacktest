import unittest
from pythonbacktest.indicator import DataDifference
import math


class DataDifferenceTests(unittest.TestCase):

    def test_number_set_individual_numbers(self):

        input_values_1 = [1, 4, 7, 2, 8, 12, 14, 16]
        input_values_2 = [3, 1, 7, 0, 2, 3, 8, 6]

        all_expected_results = [t - k for (t, k) in zip(input_values_1, input_values_2)]
        expected_result = input_values_1[-1] - input_values_2[-1]

        data_difference = DataDifference()

        for value_1, value_2 in zip(input_values_1, input_values_2):
            data_difference.on_new_upstream_value(value_1, value_2)

        all_actual_results = data_difference.all_result
        actual_result = data_difference.result

        self.assertEqual(all_expected_results, all_actual_results)
        self.assertEqual(expected_result, actual_result)

    def test_number_set_list_numbers(self):

        input_values_1 = [1, 4, 7, 2, 8, 12, 14, 16]
        input_values_2 = [3, 1, 7, 0, 2, 3, 8, 6]

        all_expected_results = [t - k for (t, k) in zip(input_values_1, input_values_2)]
        expected_result = input_values_1[-1] - input_values_2[-1]

        data_difference = DataDifference()

        data_difference.on_new_upstream_value(input_values_1, input_values_2)

        all_actual_results = data_difference.all_result
        actual_result = data_difference.result

        self.assertEqual(all_expected_results, all_actual_results)
        self.assertEqual(expected_result, actual_result)