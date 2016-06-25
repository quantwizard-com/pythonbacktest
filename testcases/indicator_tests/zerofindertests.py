import unittest
from pythonbacktest.indicator import ZeroFinder
import math

class ZeroFinderTests(unittest.TestCase):

    def test_growing_line_list_values(self):

        input_values = [-5, -4, -3, -2, -1, -1, 0, 1, 2, 3, 4, 5]
        expected_all_results = [None, -math.log(4.0 + 1, 2), -2.0, -math.log(2.0 + 1, 2), \
                                -1.0, None, 0.0, None, None, None, None, None]
        expected_result = None

        zero_finder = ZeroFinder()

        zero_finder.on_new_upstream_value(input_values)

        actual_all_results = zero_finder.all_result
        actual_result = zero_finder.result

        self.assertEqual(expected_all_results, actual_all_results)
        self.assertEqual(expected_result, actual_result)

    def test_growing_and_falling_line_list_values(self):

        input_values = [-5, -4, -3, -2, -1, -1, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
        expected_all_results = [None, -math.log(4.0 + 1, 2), -2.0, -math.log(2.0 + 1, 2),\
                                -1.0, None, 0.0, None, None, None, None, None,\
                                math.log(4.0 + 1, 2), 2.0, math.log(2.0 + 1, 2), 1.0, 0.0]

        expected_result = 0

        zero_finder = ZeroFinder()

        zero_finder.on_new_upstream_value(input_values)

        actual_all_results = zero_finder.all_result
        actual_result = zero_finder.result

        self.assertEqual(expected_all_results, actual_all_results)
        self.assertEqual(expected_result, actual_result)

