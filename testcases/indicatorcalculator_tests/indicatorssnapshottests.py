import unittest

from pythonbacktest.indicatorcalculator import IndicatorsSnapshot
import datetime


class IndicatorsSnapshotTests(unittest.TestCase):

    def test_no_data(self):
        timestamp = datetime.datetime.now()

        indicators_snapshot = IndicatorsSnapshot(timestamp)

        expected_result = {}
        actual_result = indicators_snapshot.snapshot_data

        self.assertEqual(expected_result, actual_result)

    def test_1_indicator(self):
        timestamp = datetime.datetime.now()
        indicator_name = 'indicator1'
        indicator_values = [1, 2, 3, 4, 5]

        indicators_snapshot = IndicatorsSnapshot(timestamp)
        indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name, indicator_values)

        expected_result = {indicator_name: indicator_values}
        actual_result = indicators_snapshot.snapshot_data

        self.assertEqual(expected_result, actual_result)

    def test_2_indicators(self):
        timestamp = datetime.datetime.now()
        indicator_name1 = 'indicator1'
        indicator_name2 = 'indicator2'
        indicator_values1 = [1, 2, 3, 4, 5]
        indicator_values2 = [10, 20, 30, 40, 50]

        indicators_snapshot = IndicatorsSnapshot(timestamp)
        indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name1, indicator_values1)
        indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name2, indicator_values2)

        expected_result = {indicator_name1: indicator_values1, indicator_name2: indicator_values2}
        actual_result = indicators_snapshot.snapshot_data

        self.assertEqual(expected_result, actual_result)

    def test_1_indicator_list_of_dictionaries(self):
        timestamp = datetime.datetime.now()
        indicator_name1 = 'indicator1'
        indicator_values1 = [1, 2, 3, 4, 5]

        indicators_snapshot = IndicatorsSnapshot(timestamp)
        indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name1, indicator_values1)

        expected_result = [
                {
                    indicator_name1: 1
                },
                {
                    indicator_name1: 2
                },
                {
                    indicator_name1: 3
                },
                {
                    indicator_name1: 4
                },
                {
                    indicator_name1: 5
                },
            ]

        actual_result = indicators_snapshot.snapshot_data_list

        self.assertEqual(expected_result, actual_result)

    def test_2_indicators_list_of_dictionaries(self):
        timestamp = datetime.datetime.now()
        indicator_name1 = 'indicator1'
        indicator_values1 = [1, 2, 3, 4, 5]
        indicator_name2 = 'indicator2'
        indicator_values2 = [10, 20, 30, 40, 50]

        indicators_snapshot = IndicatorsSnapshot(timestamp)
        indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name1, indicator_values1)
        indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name2, indicator_values2)

        expected_result = [
            {
                indicator_name1: 1, indicator_name2: 10
            },
            {
                indicator_name1: 2, indicator_name2: 20
            },
            {
                indicator_name1: 3, indicator_name2: 30
            },
            {
                indicator_name1: 4, indicator_name2: 40
            },
            {
                indicator_name1: 5, indicator_name2: 50
            },
        ]

        actual_result = indicators_snapshot.snapshot_data_list

        self.assertEqual(expected_result, actual_result)
