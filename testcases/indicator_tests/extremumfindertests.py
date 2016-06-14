import unittest
from pythonbacktest.indicator import ExtremumFinder

class ExtremumFinderTests(unittest.TestCase):

    def test_growing_line_list_values(self):

        input_values = [1, 2, 3, 4, 5]
        expected_all_results = [None, None, None, None, None]
        expected_result = None

        extremum_finder = ExtremumFinder()

        extremum_finder.on_new_upstream_value(input_values)

        actual_all_results = extremum_finder.all_result
        actual_result = extremum_finder.result

        self.assertEqual(expected_all_results, actual_all_results)
        self.assertEqual(expected_result, actual_result)

    def test_x2_list_values(self):

        input_values = [16, 9, 4, 1, 0, 1, 4, 9]
        expected_all_results = [None, None, 2.5, 1.5, 0.5, None, None, None]
        expected_result = None

        extremum_finder = ExtremumFinder()

        extremum_finder.on_new_upstream_value(input_values)

        actual_all_results = extremum_finder.all_result
        actual_result = extremum_finder.result

        self.assertEqual(expected_all_results, actual_all_results)
        self.assertEqual(expected_result, actual_result)
