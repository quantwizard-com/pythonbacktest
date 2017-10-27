import unittest
from unittest.mock import MagicMock

from pythonbacktest.indicator import DataCrossIndicator


class DataCrossIndicatorTests(unittest.TestCase):

    def test_number_set_individual_numbers(self):
        source_indicator_mock = MagicMock()

        input_values_1 =       [3, 2, 1, 2, 3, 4, 5, 6]
        input_values_2 =       [3, 4, 2, 1, 0, 1, 2, 3]
                              # N,
        all_expected_results = [None, 0, 0, 1, 0, 0, 0, 0]
        expected_result = 0

        data_cross = DataCrossIndicator(indicator_name='DataCross', source_indicators=source_indicator_mock)

        for value_1, value_2 in zip(input_values_1, input_values_2):
            source_indicator_mock.get_latest_result = MagicMock(return_value=(value_1, value_2))
            data_cross.new_upstream_record()

        all_actual_results = data_cross.all_results
        actual_result = data_cross.latest_result

        self.assertEqual(all_expected_results, all_actual_results)
        self.assertEqual(expected_result, actual_result)

    def test_number_set_individual_numbers_with_None(self):
        source_indicator_mock = MagicMock()

        input_values_1 =       [None, None, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6]
        input_values_2 =       [None, None, 1, 2, 3, 4, 2, 1, 0, 1, 2, 3]
                               # N,    N,   N, >, =, <, <, >, >, >, >, >
        all_expected_results = [None, None, None, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        expected_result = 0

        data_cross = DataCrossIndicator(indicator_name='DataCross', source_indicators=source_indicator_mock)

        for value_1, value_2 in zip(input_values_1, input_values_2):
            source_indicator_mock.get_latest_result = MagicMock(return_value=(value_1, value_2))
            data_cross.new_upstream_record()

        all_actual_results = data_cross.all_results
        actual_result = data_cross.latest_result

        self.assertEqual(all_expected_results, all_actual_results)
        self.assertEqual(expected_result, actual_result)