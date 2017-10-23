import unittest
from unittest.mock import MagicMock

from pythonbacktest.indicator import SMA


class SmaTests(unittest.TestCase):

    def test_sma_3_individual_values(self):
        sma_source_indicator_mock = MagicMock()
        input_data = [1, 12, 26, 4, 6, -4]
        expected_result = [None, None, 13, 14, 12, 2]

        sma = SMA(indicator_name='SMA', window_len=3, source_indicators=sma_source_indicator_mock)

        for input_record in input_data:
            sma_source_indicator_mock.get_latest_result = MagicMock(return_value=input_record)
            sma.new_upstream_record()

        self.assertEqual(expected_result[-1], sma.latest_result)
        self.assertEqual(expected_result, sma.all_results)

    def test_sma_3_individual_values_leading_nones(self):
        sma_source_indicator_mock = MagicMock()
        input_data = [None, None, 1, 12, 26, 4, 6, -4]
        expected_result = [None, None, None, None, 13, 14, 12, 2]

        sma = SMA(indicator_name='SMA', window_len=3, source_indicators=sma_source_indicator_mock)

        for input_record in input_data:
            sma_source_indicator_mock.get_latest_result = MagicMock(return_value=input_record)
            sma.new_upstream_record()

        self.assertEqual(expected_result[-1], sma.latest_result)
        self.assertEqual(expected_result, sma.all_results)

    def test_sma_3_individual_values_middle_nones(self):
        sma_source_indicator_mock = MagicMock()
        input_data = [1, None, 12, 26, 4, None, 6, -4]
        expected_result = [None, None, None, 13, 14, None, 12, 2]

        sma = SMA(indicator_name='SMA', window_len=3, source_indicators=sma_source_indicator_mock)

        for input_record in input_data:
            sma_source_indicator_mock.get_latest_result = MagicMock(return_value=input_record)
            sma.new_upstream_record()

        self.assertEqual(expected_result[-1], sma.latest_result)
        self.assertEqual(expected_result, sma.all_results)

