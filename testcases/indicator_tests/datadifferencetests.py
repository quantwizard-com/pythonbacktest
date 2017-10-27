import unittest
from unittest.mock import MagicMock

from pythonbacktest.indicator import DataDifference


class DataDifferenceTests(unittest.TestCase):

    def test_number_set_individual_numbers(self):
        source_indicator_mock = MagicMock()

        input_values_1 = [None, None, 1, 4, None, 2, 8, 12, 14, None, 1]
        input_values_2 = [None, None, 3, 1, None, 0, None, 3, 8, 6, 2]

        all_expected_results = [v2 - v1 if None not in (v1, v2) else None for (v1, v2) in zip(input_values_1, input_values_2)]
        expected_result = input_values_2[-1] - input_values_1[-1]

        data_difference = DataDifference(indicator_name='DataDifference', source_indicators=source_indicator_mock)

        for value_1, value_2 in zip(input_values_1, input_values_2):
            source_indicator_mock.get_latest_result = MagicMock(return_value=(value_1, value_2))
            data_difference.new_upstream_record()

        all_actual_results = data_difference.all_results
        actual_result = data_difference.latest_result

        self.assertEqual(all_expected_results, all_actual_results)
        self.assertEqual(expected_result, actual_result)