import unittest
from pythonbacktest.indicator import ChangeTracker


class DataDelayTests(unittest.TestCase):

    def test_changetracking_individual_values_single_value(self):

        test_data = [1]
        single_delay = 3

        expected_result = [None]
        change_tracker = ChangeTracker(delay_size=single_delay)

        # insert individual values
        for test_number in test_data:
            change_tracker.on_new_upstream_value(test_number)

        self.assertEqual(expected_result, change_tracker.all_result)

    def test_changetracking_individual_values_single_none_value(self):

        test_data = [None]
        single_delay = 3

        expected_result = [None]
        change_tracker = ChangeTracker(delay_size=single_delay)

        # insert individual values
        for test_number in test_data:
            change_tracker.on_new_upstream_value(test_number)

        self.assertEqual(expected_result, change_tracker.all_result)


    def test_changetracking_individual_values_multiple_values_zero_delay(self):

        test_data = [1, 2, 5, 6, 10, 8]
        single_delay = 0

        expected_result = [0, 0, 0, 0, 0, 0]
        change_tracker = ChangeTracker(delay_size=single_delay)

        # insert individual values
        for test_number in test_data:
            change_tracker.on_new_upstream_value(test_number)

        self.assertEqual(expected_result, change_tracker.all_result)

    def test_changetracking_individual_values_multiple_values_nonzero_delay(self):

        test_data = [1, 2, 5, 6, 10, 8]
        single_delay = 3

        expected_result = [None, None, None, 5, 8, 3]
        change_tracker = ChangeTracker(delay_size=single_delay)

        # insert individual values
        for test_number in test_data:
            change_tracker.on_new_upstream_value(test_number)

        self.assertEqual(expected_result, change_tracker.all_result)


    def test_changetracking_individual_values_multiple_values_leading_nones(self):

        test_data = [None, None, 1, 2, 3, 4, 5]
        single_delay = 2

        expected_result = [None, None, None, None, 2, 2, 2]

        change_tracker = ChangeTracker(delay_size=single_delay)

        # insert individual values
        for test_number in test_data:
            change_tracker.on_new_upstream_value(test_number)

        self.assertEqual(expected_result, change_tracker.all_result)
