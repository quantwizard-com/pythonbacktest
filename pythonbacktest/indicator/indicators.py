from .staticvalue import StaticValue


class Indicators(object):

    def __init__(self):
        self.__all_indicators = {}

        # set static values for price bar values
        for price_bar_field in ["open", "close", "high", "low", "volume"]:
            self.__all_indicators[price_bar_field] = (None, StaticValue())

    # indicators - collection of tuples with following fields:
    # name - indicator name
    # input name - name of the indicator, which should be an input for the given indicator
    # implementation - implementation of the indicator
    def init_indicators(self, indicators):

        for name, input_name, implementation in indicators:

            if name in self.__all_indicators:
                raise ValueError("Indicator with name '%s' is already declared" % name)

            if input_name is None or implementation is None:
                raise ValueError("Either input_name or implementation is null")

            self.__all_indicators[name] = (input_name, implementation)

    # a new price bar has arrived
    # that will trigger operatotion of moving through all the indicators
    # passing values in and calculating outcomes
    def new_price_bar(self, price_bar):

        if price_bar is None:
            raise ValueError("price_bar is null")

        self.__update_static_values(price_bar)

        # move through all listed indicators and calculate all of those
        for indicator_name, source_name, indicator in self.__all_indicators:

            if source_name is not None:
                current_value_at_source = self[source_name]

                indicator.on_new_upstream_value(current_value_at_source)


    def __update_static_values(self, price_bar):
        field_values = {"open": price_bar.open, "close": price_bar.close,
                        "high": price_bar.high, "low": price_bar.low,
                        "volume": price_bar.volume }

        for key, value in field_values:
            # these are all static values, so the only impact here is recording new values
            self.__all_indicators[key][1].on_new_upstream_value(value)


    # get current value for the indicator name
    def __getitem__(self, indicator_name):
        return self.__all_indicators[indicator_name].result
