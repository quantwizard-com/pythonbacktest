import unittest
from pythonbacktest.indicator import DataProcessor

class DataProcessorTests(unittest.TestCase):

    def test_sample_filter_remove_negative_values_single_entries(self):

        test_data = [t for t in range(-5, 5)]
        expected_result = [0 if t < 0 else t for t in test_data]
        processor_function = lambda x: 0 if x < 0 else x

        indicator = DataProcessor(processor_function)

        for test_record in test_data:
            indicator.on_new_upstream_value(test_record)

        self.assertEqual(expected_result, indicator.all_result)

if __name__ == "__main__":
    unittest.main()
