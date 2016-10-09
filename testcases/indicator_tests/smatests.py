import unittest

from pythonbacktest.indicator import SMA


class SmaTests(unittest.TestCase):

    def test_sma_3_individual_values(self):
        input_data = [1, 12, 26, 4, 6, -4]
        expected_result = [None, None, 13, 14, 12, 2]

        sma = SMA(3)

        for input_record in input_data:
            sma.on_new_upstream_value(input_record)

        self.assertEqual(expected_result[-1], sma.result)
        self.assertEqual(expected_result, sma.all_result)

    def test_sma_3_individual_values_leading_nones(self):
        input_data = [None, None, 1, 12, 26, 4, 6, -4]
        expected_result = [None, None, None, None, 13, 14, 12, 2]

        sma = SMA(3)

        for input_record in input_data:
            sma.on_new_upstream_value(input_record)

        self.assertEqual(expected_result[-1], sma.result)
        self.assertEqual(expected_result, sma.all_result)

    def test_sma_3_individual_values_middle_nones(self):
        input_data = [1, None, 12, 26, 4, None, 6, -4]
        expected_result = [None, None, None, 13, 14, None, 12, 2]

        sma = SMA(3)

        for input_record in input_data:
            sma.on_new_upstream_value(input_record)

        self.assertEqual(expected_result[-1], sma.result)
        self.assertEqual(expected_result, sma.all_result)

