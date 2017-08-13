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

