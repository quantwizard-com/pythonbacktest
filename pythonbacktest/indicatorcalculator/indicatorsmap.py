from . import IndicatorsMapIndicatorRecord
from pythonbacktest.indicator import PriceBarIndicator, StaticValue


class IndicatorsMap(object):

    def __init__(self, indicators_map_definition=None):
        self.__all_indicators = []
        self.__name_to_indicator_map = {}
        self.__price_bar_indicator = None

        self.apply_map_definition(indicators_map_definition)

    def apply_map_definition(self, indicators_map_definition):
        self.__all_indicators = []
        self.__name_to_indicator_map = {}
        self.__price_bar_indicator = None

        self.__add_static_indicators()

        if not indicators_map_definition:
            return

        for record in indicators_map_definition:
            indicator_name, source_specs, indicator_implementation = self.__unpack_input_map_record(record)
            source_implementations = self.__source_specs_to_source_implementations(source_specs)

            indicator_implementation.set_source_indicators(source_implementations)

            self.__name_to_indicator_map[indicator_name] = indicator_implementation
            self.__all_indicators.append(indicator_implementation)

    def new_price_bar(self, price_bar):
        self.__price_bar_indicator.inject_new_price_bar(price_bar)
        self.__propagate_new_price_bar_event()

    def __propagate_new_price_bar_event(self):
        for indicator in self.__all_indicators:
            indicator.new_upstream_record()

    def __add_static_indicators(self):
        price_bar_indicator = PriceBarIndicator()
        self.__price_bar_indicator = price_bar_indicator

        timestamp_indicator = StaticValue(source_indicators=[(price_bar_indicator, 'timestamp')])
        open_indicator = StaticValue(source_indicators=[(price_bar_indicator, 'open')])
        close_indicator = StaticValue(source_indicators=[(price_bar_indicator, 'close')])
        high_indicator = StaticValue(source_indicators=[(price_bar_indicator, 'high')])
        low_indicator = StaticValue(source_indicators=[(price_bar_indicator, 'low')])
        volume_indicator = StaticValue(source_indicators=[(price_bar_indicator, 'volume')])

        self.__name_to_indicator_map = {
            'pricebar': price_bar_indicator,
            'timestamp': timestamp_indicator,
            'open': open_indicator,
            'close': close_indicator,
            'high': high_indicator,
            'low': low_indicator,
            'volume': volume_indicator
        }

        self.__all_indicators=[price_bar_indicator, timestamp_indicator, open_indicator,
                               close_indicator, high_indicator, low_indicator, volume_indicator]

    def all_indicators(self):
        return self.__all_indicators

    def __unpack_input_map_record(self, input_record):
        indicator_name = input_record['name']
        source_specs = input_record['sources']
        implementation = input_record['implementation']

        if indicator_name in self.__name_to_indicator_map:
            raise ValueError("Indicator with name '%s' is already declared" % indicator_name)

        if source_specs is None or implementation is None:
            raise ValueError("Either input_name or implementation is None")

        if not source_specs:
            raise ValueError("Source specs are not set")

        return indicator_name, source_specs, implementation

    def __source_specs_to_source_implementations(self, source_specs):

        source_implementations = []

        # simple case - we have just a single string
        if isinstance(source_specs, str):
            source_specs = [source_specs]

        for source_spec in source_specs:
            indicator_name = None
            indicator_string_reference = None

            if isinstance(source_spec, tuple):
                indicator_name, indicator_string_reference = source_spec
            else:
                indicator_name = source_spec

            if indicator_name not in self.__name_to_indicator_map:
                raise ValueError(f"Can't find definition of the indicator {indicator_name}")

            indicator_implementation = self.__name_to_indicator_map[indicator_name]

            source_implementations.append(
                indicator_implementation if indicator_string_reference is None
                else (indicator_implementation, indicator_string_reference))

