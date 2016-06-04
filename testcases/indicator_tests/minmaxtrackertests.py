import unittest
from pythonbacktest.indicator import MinMaxTracker


class MinMaxTrackerTests(unittest.TestCase):

    def test_add_single_collection(self):

        test_data = [1, 2, 3, 4, 5, 6]
        expected_result = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]

        min_max_tracker = MinMaxTracker()
        min_max_tracker.on_new_upstream_value(test_data)

        actual_result = min_max_tracker.all_result

        self.assertEqual(expected_result, actual_result)

    def test_add_2_collections_the_same_legth(self):

        test_data1 = [1, 2, 3, 4, 5, 6]
        test_data2 = [6, 5, 4, 3, 2, 1]

        expected_result = [(1, 6), (2, 5), (3, 4), (3, 4), (2, 5), (1, 6)]

        min_max_tracker = MinMaxTracker()
        min_max_tracker.on_new_upstream_value(test_data1)
        min_max_tracker.on_new_upstream_value(test_data2)

        actual_result = min_max_tracker.all_result

        self.assertEqual(expected_result, actual_result)

