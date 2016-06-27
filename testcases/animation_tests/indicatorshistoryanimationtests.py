import unittest
from pythonbacktest.animation import IndicatorsHistoryAnimation
import numpy as np

class IndicatorsHistoryAnimationTests(unittest.TestCase):

    def test_pack_data_with_index_flat_list(self):

        input_data = [1, 2, 3, 4, 5]

        expected_output = ([0, 1, 2, 3, 4], np.array(input_data))

        actual_output = IndicatorsHistoryAnimation._IndicatorsHistoryAnimation__pack_data_with_index(input_data)

        self.assertEqual(expected_output[0], actual_output[0])
        self.assertEqual(expected_output[1].tolist(), actual_output[1].tolist())

    def test_pack_data_with_index_flat_list_2nones(self):

        input_data = [1, None, 3, None, 5]

        expected_output = ([0, 1, 2, 3, 4], np.array([1, np.nan, 3, np.nan, 5]))

        actual_output = IndicatorsHistoryAnimation._IndicatorsHistoryAnimation__pack_data_with_index(input_data)

        self.assertEqual(expected_output[0], actual_output[0])
        np.testing.assert_equal(actual_output[1], expected_output[1])

    def test_pack_data_with_index_tuple_list(self):

        input_data = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

        expected_output = ([0, 1, 2, 0, 0, 1, 2, 0, 0, 1, 2], np.array([1, 4, 7, np.nan, 2, 5, 8, np.nan, 3, 6, 9]))

        actual_output = IndicatorsHistoryAnimation._IndicatorsHistoryAnimation__pack_data_with_index(input_data)

        self.assertEqual(expected_output[0], actual_output[0])
        np.testing.assert_equal(expected_output[1], actual_output[1])

    def test_pack_data_with_index_tuple_list_1none(self):

        input_data = [(1, 2, 3), (4, 5, 6), None, (7, 8, 9)]

        expected_output = ([0, 1, 2, 3, 0, 0, 1, 2, 3, 0, 0, 1, 2, 3],
                           np.array([1, 4, np.nan, 7, np.nan, 2, 5, np.nan, 8, np.nan, 3, 6, np.nan, 9]))

        actual_output = IndicatorsHistoryAnimation._IndicatorsHistoryAnimation__pack_data_with_index(input_data)

        self.assertEqual(expected_output[0], actual_output[0])
        np.testing.assert_equal(expected_output[1], actual_output[1])


