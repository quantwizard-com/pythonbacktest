import unittest
from datetime import datetime

from pythonbacktest.datafeed import AbstractDataFeed
from pythonbacktest.datafeed import TradingDayData


class DataDelayTests(unittest.TestCase):

    def test_get_all_data(self):

        input_data = [1,2,3,4,5,6]
        data_date = datetime(2016, 12, 12, 14, 53, 11)

        data_feed = AbstractDataFeed()
        data_feed.all_data[data_date] = TradingDayData(input_data, data_date)

        actual_data = data_feed.get_prices_bars_for_day(data_date)

        self.assertEqual(actual_data, input_data)

    def test_all_elements_by_view_range(self):

        input_data = [1,2,3,4,5,6]
        expected_data = [1,2,3,4,5,6]
        data_date = datetime(2016, 12, 12, 14, 53, 11)

        data_feed = AbstractDataFeed()
        data_feed.all_data[data_date] = TradingDayData(input_data, data_date)
        data_feed.set_data_view_range(0, 5)

        actual_data = data_feed.get_prices_bars_for_day(data_date)

        self.assertEqual(actual_data, expected_data)

    def test_get_first_4_elements(self):

        input_data = [1,2,3,4,5,6]
        expected_data = [1,2,3,4]
        data_date = datetime(2016, 12, 12, 14, 53, 11)

        data_feed = AbstractDataFeed()
        data_feed.all_data[data_date] = TradingDayData(input_data, data_date)
        data_feed.set_data_view_range(0, 3)

        actual_data = data_feed.get_prices_bars_for_day(data_date)

        self.assertEqual(actual_data, expected_data)

    def test_get_last_5_elements(self):

        input_data = [1,2,3,4,5,6]
        expected_data = [2,3,4,5,6]
        data_date = datetime(2016, 12, 12, 14, 53, 11)

        data_feed = AbstractDataFeed()
        data_feed.all_data[data_date] = TradingDayData(input_data, data_date)
        data_feed.set_data_view_range(1, 5)

        actual_data = data_feed.get_prices_bars_for_day(data_date)

        self.assertEqual(actual_data, expected_data)

    def test_get_middle_2_elements(self):

        input_data = [1,2,3,4,5,6]
        expected_data = [4,5]
        data_date = datetime(2016, 12, 12, 14, 53, 11)

        data_feed = AbstractDataFeed()
        data_feed.all_data[data_date] = TradingDayData(input_data, data_date)
        data_feed.set_data_view_range(3, 4)

        actual_data = data_feed.get_prices_bars_for_day(data_date)

        self.assertEqual(actual_data, expected_data)

    def test_get_middle_1_element(self):

        input_data = [1,2,3,4,5,6]
        expected_data = [3]
        data_date = datetime(2016, 12, 12, 14, 53, 11)

        data_feed = AbstractDataFeed()
        data_feed.all_data[data_date] = TradingDayData(input_data, data_date)
        data_feed.set_data_view_range(2, 2)

        actual_data = data_feed.get_prices_bars_for_day(data_date)

        self.assertEqual(actual_data, expected_data)