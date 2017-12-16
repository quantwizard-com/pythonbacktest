import unittest
from unittest.mock import MagicMock

from pythonbacktest.datafeed import PriceBar
from pythonbacktest.indicator import AggregatedPriceBar, PriceBarIndicator


class AggregatedPriceBarTests(unittest.TestCase):

    def test_aggregation_no_number_of_pricebars_defined(self):

        price_bar_1 = {
            'timestamp': 1111,
            'open': 12,
            'close': 13,
            'high': 14,
            'low': 15,
            'volume': 100
        }

        price_bar_2 = {
            'timestamp': 2222,
            'open': 22,
            'close': 23,
            'high': 24,
            'low': 5,
            'volume': 200
        }

        price_bar_source_indicator_mock = MagicMock(spec=PriceBarIndicator)

        input_price_bars = [price_bar_1, price_bar_2]
        apb = AggregatedPriceBar(indicator_name='APB', source_indicators=price_bar_source_indicator_mock)

        for price_bar in input_price_bars:
            price_bar_source_indicator_mock.get_latest_result = MagicMock(return_value=price_bar)
            apb.new_upstream_record()

        calculated_price_bar = apb.latest_result

        self.assertEqual(1111, calculated_price_bar.timestamp)
        self.assertEqual(12, calculated_price_bar.open)
        self.assertEqual(23, calculated_price_bar.close)
        self.assertEqual(24, calculated_price_bar.high)
        self.assertEqual(5, calculated_price_bar.low)
        self.assertEqual(300, calculated_price_bar.volume)
