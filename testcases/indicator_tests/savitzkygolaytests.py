import unittest
import random
from pythonbacktest.indicator import SavitzkyGolay
from scipy.signal import savgol_filter

class SavitzkyGolayTests(unittest.TestCase):

    def test_10singlevalues(self):
        sg_indicator = SavitzkyGolay(window_size=3, polyorder=1, level=1)

        test_data = [t for t in range(0, 9)]

        for record in test_data:
            sg_indicator.on_new_upstream_value(record)

        self.assertEqual(test_data, sg_indicator._SavitzkyGolay__data_storage)
        self.assertEqual(len(test_data), len(sg_indicator.all_result))

    def test_10growing_list(self):
        sg_indicator = SavitzkyGolay(window_size=3, polyorder=1, level=1)

        test_data = []
        for i in range(1, 11):
            test_data.append([s for s in range(0, i)])

        for test_record in test_data:
            sg_indicator.on_new_upstream_value(test_record)
            self.assertEqual(test_record, sg_indicator._SavitzkyGolay__data_storage)

    def test_10elements_list_1none(self):
        sg_indicator = SavitzkyGolay(window_size=3, polyorder=1, level=1)

        test_data = [None] + [t for t in range(1, 9)]
        sg_indicator.on_new_upstream_value(test_data)

        self.assertEqual(test_data, sg_indicator._SavitzkyGolay__data_storage)
        self.assertEqual(len(test_data), len(sg_indicator.all_result))
        self.assertIsNone(sg_indicator.all_result[0])

    def test_10elements_list_5nones(self):
        sg_indicator = SavitzkyGolay(window_size=3, polyorder=1, level=1)

        test_data = [None] * 5 + [t for t in range(1, 9)]
        sg_indicator.on_new_upstream_value(test_data)

        self.assertEqual(test_data, sg_indicator._SavitzkyGolay__data_storage)
        self.assertEqual(len(test_data), len(sg_indicator.all_result))
        self.assertEqual([None] * 5, sg_indicator.all_result[0:5])

    def test_100elements_list_with_real_data(self):
        WINDOW_SIZE = 21
        POLYORDER = 1

        sg_indicator = SavitzkyGolay(window_size=WINDOW_SIZE, polyorder=POLYORDER, level=1)

        input_data = [random.randint(0, 20) for x in range(100)]
        expected_result = savgol_filter(input_data, window_length=WINDOW_SIZE, polyorder=POLYORDER)
        expected_result = list(expected_result)

        # execute
        sg_indicator.on_new_upstream_value(input_data)
        actual_result = sg_indicator.all_result

        # we're interested only in single thing: do the results match?
        self.assertEqual(expected_result, actual_result)

    def test_100elements_list_with_growing_data_passed_collection(self):

        WINDOW_SIZE = 21
        POLYORDER = 1
        EXPERIMENTS = 100

        input_data = [random.randint(0, 20) for x in range(100)]
        sg_indicator = SavitzkyGolay(window_size=WINDOW_SIZE, polyorder=POLYORDER, level=1)

        for i in range(0, 100):

            input_data.append(random.randint(0, 20))

            expected_result = savgol_filter(input_data, window_length=WINDOW_SIZE, polyorder=POLYORDER)
            expected_result = list(expected_result)

            # execute
            sg_indicator.on_new_upstream_value(input_data)
            actual_result = sg_indicator.all_result

            # we're interested only in single thing: do the results match?
            self.assertEqual(expected_result, actual_result)

    def test_100elements_list_with_growing_data_passed_single_int(self):

        WINDOW_SIZE = 21
        POLYORDER = 1
        EXPERIMENTS = 4600

        input_data = []
        sg_indicator = SavitzkyGolay(window_size=WINDOW_SIZE, polyorder=POLYORDER, level=1)

        for i in range(0, EXPERIMENTS):

            random_int = random.randint(0, 20)
            input_data.append(random_int)

            expected_result = [None] * len(input_data) if len(input_data) < WINDOW_SIZE \
                else savgol_filter(input_data, window_length=WINDOW_SIZE, polyorder=POLYORDER)

            expected_result = list(expected_result)

            # execute
            sg_indicator.on_new_upstream_value(random_int)
            actual_result = sg_indicator.all_result

            # we're interested only in single thing: do the results match?
            self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
