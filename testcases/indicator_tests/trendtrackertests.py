import unittest
from pythonbacktest.indicator import TrendTracker


class TrendTrackerTests(unittest.TestCase):

    def test_none_values_in_input(self):
        test_data = [None, None, None, None, None]
        expected_result = [(None, None), (None, None), (None, None), (None, None), (None, None)]

        trend_tracker = TrendTracker()

        for test_record in test_data:
            trend_tracker.on_new_upstream_value(test_record)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)

    def test_single_support_point(self):
        test_data = [5, 4, 3, 4, 5]
        expected_result = [(None, None), (None, None), (3, None), (None, None), (None, None)]

        trend_tracker = TrendTracker()

        trend_tracker.on_new_upstream_value(test_data)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)

    def test_single_support_point_mix_with_nones(self):
        test_data = [None, 5, 4, None, None, 3, None, 4, 5, None]
        expected_result = \
            [(None, None), (None, None),
             (None, None), (None, None),
             (None, None), (3, None),
             (None, None), (None, None),
             (None, None), (None, None)]

        trend_tracker = TrendTracker()

        trend_tracker.on_new_upstream_value(test_data)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)

    def test_single_resistance_point(self):
        test_data = [3, 4, 5, 4, 3]
        expected_result = [(None, None), (None, None), (None, 5), (None, None), (None, None)]

        trend_tracker = TrendTracker()
        trend_tracker.on_new_upstream_value(test_data)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)

    def test_single_resistance_point_with_a_few_constants(self):
        test_data = [3, 3, 5, 5, 4, 3, 3]
        expected_result = [(None, None), (None, None), (None, None), (None, 5), (None, None), (None, None), (None, None)]

        trend_tracker = TrendTracker()
        trend_tracker.on_new_upstream_value(test_data)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)


    def test_resistance_then_support(self):
        test_data = [3, 4, 5, 4, 3, 2, 1, 2, 3, 4]
        expected_result = [
            (None, None), (None, None), (None, 5),
            (None, None), (None, None), (None, None),
            (1, None), (None, None), (None, None), (None, None)]

        trend_tracker = TrendTracker()
        trend_tracker.on_new_upstream_value(test_data)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)

    def test_rapid_changes(self):
        test_data = [3, 4, 3, 4, 3, 4, 3]
        expected_result = [
            (None, None), (None, 4), (3, None), (None, 4), (3, None), (None, 4), (None, None)
        ]

        trend_tracker = TrendTracker()
        trend_tracker.on_new_upstream_value(test_data)

        actual_result = trend_tracker.all_result

        self.assertEqual(expected_result, actual_result)