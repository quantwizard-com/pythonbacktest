import unittest
from pythonbacktest.indicator import Differential

class DifferentialTests(unittest.TestCase):

    def test_differential_individual_values(self):

        test_data = [1, 2, 3, 4, 2, 0, -2, -5]
        expected_result = [None, 1, 1, 1, -2, -2, -2, -3]

        indicator = Differential()

        for test_record in test_data:
            indicator.on_new_upstream_value(test_record)

        self.assertEqual(expected_result, indicator.all_result)

    def test_differential_individual_values_leading_nones(self):

        test_data = [None, None, None, None, 1, 2, 3, 4, 2, 0, -2, -5]
        expected_result = [None, None, None, None, None, 1, 1, 1, -2, -2, -2, -3]

        indicator = Differential()

        for test_record in test_data:
            indicator.on_new_upstream_value(test_record)

        self.assertEqual(expected_result, indicator.all_result)

    def test_differential_collection_single_value(self):

        test_data = [1]
        expected_result = [None]

        indicator = Differential()

        indicator.on_new_upstream_value(test_data)
        self.assertEqual(expected_result, indicator.all_result)

        indicator.on_new_upstream_value(test_data)
        self.assertEqual(expected_result, indicator.all_result)


    def test_differential_collection(self):

        test_data = [1, 2, 3, 4, 2, 0, -2, -5]
        expected_result = [None, 1, 1, 1, -2, -2, -2, -3]

        indicator = Differential()

        indicator.on_new_upstream_value(test_data)
        self.assertEqual(expected_result, indicator.all_result)

        indicator.on_new_upstream_value(test_data)
        self.assertEqual(expected_result, indicator.all_result)

    def test_differential_collection_leading_nones(self):

        test_data = [None, None, None, None, 1, 2, 3, 4, 2, 0, -2, -5]
        expected_result = [None, None, None, None, None, 1, 1, 1, -2, -2, -2, -3]

        indicator = Differential()

        indicator.on_new_upstream_value(test_data)
        self.assertEqual(expected_result, indicator.all_result)

        indicator.on_new_upstream_value(test_data)
        self.assertEqual(expected_result, indicator.all_result)
