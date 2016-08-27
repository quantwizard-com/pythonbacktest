import unittest
from pythonbacktest.indicator import DataDelay

class DataDelayTests(unittest.TestCase):

    def test_delay_individual_values(self):

        test_data = [None, None, 1, 2, 3, 4, 5]
        delay = range(0, 5)

        for single_delay in delay:
            expected_result = (single_delay * [None] + test_data[0:-single_delay]) if single_delay != 0 else test_data

            delay_indicator = DataDelay(delay_size=single_delay)

            # insert individual values
            for test_number in test_data:
                delay_indicator.on_new_upstream_value(test_number)

            self.assertEqual(expected_result, delay_indicator.all_result)

    def test_delay_individual_list_on_input(self):

        test_data = [None, None, 1, 2, 3, 4, 5]
        delay = range(1, 5)

        for single_delay in delay:

            delay_indicator = DataDelay(delay_size=single_delay)

            # this is real-life scenario: to the same object add list multiple times with growing number of elements
            for test_data_length in range(4, len(test_data) + 1):
                test_subset = test_data[0:test_data_length]

                expected_result = (single_delay * [None] + test_subset[0:-single_delay]) if single_delay != 0 else test_subset

                delay_indicator.on_new_upstream_value(test_subset)
                actual_result = delay_indicator.all_result

                self.assertEqual(expected_result, actual_result)
