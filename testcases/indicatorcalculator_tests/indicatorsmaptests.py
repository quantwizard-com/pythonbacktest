import unittest

from pythonbacktest.datafeed import PriceBar
from pythonbacktest.indicator import PriceBarIndicator
from pythonbacktest.indicator import StaticValue
from pythonbacktest.indicatorcalculator import IndicatorsMap
from pythonbacktest.indicator import SMA


class IndicatorsMapTests(unittest.TestCase):

    def test_simple_map_empty_indicators_map_definition(self):
        indicators_map = IndicatorsMap()

        all_indicators = indicators_map.all_indicators()

        # we expect 7 indicators on the map:
        # - price bar indicator (aka: root indicator)
        # - static value indicators: timestamp, open, close, high, low, volume

        self.assertEqual(7, len(all_indicators))

        # first indicator on the list MUST BE the PriceBarIndicator
        self.assertTrue(isinstance(all_indicators[0], PriceBarIndicator))

    def test_simple_map_happy_path_1(self):

        indicators_map_definition = [
            {'name': 'SMA', 'sources': 'open', 'implementation': SMA(indicator_name='SMA', window_len=50)}]

        indicators_map = IndicatorsMap(indicators_map_definition)

        all_indicators = indicators_map.all_indicators()

        # we expect 8 indicators on the map:
        # - price bar indicator (aka: root indicator)
        # - static value indicators: timestamp, open, close, high, low, volume
        # - SMA

        self.assertEqual(8, len(all_indicators))

    def test_simple_map_price_bar_propagation_1(self):
        """
        Test if values of the PriceBar propagates to individual indicators
        """
        indicator_static_open_from_pricebar_name = 'static_open_from_pricebar'
        indicator_static_open_name = 'static_open'
        indicator_static_close_name = 'static_close'

        static_open_from_pricebar = StaticValue(indicator_name=indicator_static_open_from_pricebar_name)
        static_open = StaticValue(indicator_name=indicator_static_open_name)
        static_close = StaticValue(indicator_name=indicator_static_close_name)

        indicators_map_definition = [
            {'name': indicator_static_open_from_pricebar_name, 'sources': ('pricebar', 'open'),
             'implementation': static_open_from_pricebar},

            {'name': indicator_static_open_name, 'sources': 'open',
             'implementation': static_open},

            {'name': indicator_static_close_name, 'sources': 'close',
             'implementation': static_close},
        ]

        pricebar = PriceBar()
        pricebar.open = 123
        pricebar.close = 456

        indicators_map = IndicatorsMap(indicators_map_definition)
        indicators_map.new_price_bar(pricebar)

        all_indicators = indicators_map.all_indicators()

        # we expect 8 indicators on the map:
        # - price bar indicator (aka: root indicator)
        # - static value indicators: timestamp, open, close, high, low, volume
        # + 3 additional indicators

        self.assertEqual(10, len(all_indicators))

        # validate indicator values
        self.assertEqual(pricebar.open, static_open_from_pricebar.latest_result)
        self.assertEqual(pricebar.open, static_open.latest_result)
        self.assertEqual(pricebar.close, static_close.latest_result)




