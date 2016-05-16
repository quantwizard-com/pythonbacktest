from .staticvalue import StaticValue
import copy


class Indicators(object):

    ALL_STATIC_FIELDS = ["open", "close", "high", "low", "volume", "trade_sell", "trade_buy", "trade_short"]
    TRANSACTION_TO_FIELD_NAME = {"BUY": "trade_buy", "SELL": "trade_sell", "SHORT": "trade_short"}

    def __init__(self, indicators_to_copy=None):
        """
        Constructor with copying functionality
        :type indicators_to_copy: Indicators
        """
        self.__all_indicators = {}

        if indicators_to_copy is None:
            # set static values for price bar values
            for price_bar_field in self.ALL_STATIC_FIELDS:
                self.__all_indicators[price_bar_field] = (None, StaticValue())
        else:
            # indicators is not None, so we have to copy its content without changing anything
            self.__all_indicators = copy.deepcopy(indicators_to_copy.__all_indicators)

    # indicators - define collection of indicators, which should be collected during trading;
    #   collection of tuples with following fields:
    # - name - indicator name
    # - source name - name of the indicator, which should be an input for the given indicator
    # - implementation - implementation of the indicator
    def set_indicators(self, indicator_records):

        for indicator_name, source_name, implementation in indicator_records:

            if indicator_name in self.__all_indicators.iteritems():
                raise ValueError("Indicator with name '%s' is already declared" % indicator_name)

            if source_name is None or implementation is None:
                raise ValueError("Either input_name or implementation is null")

            self.__all_indicators[indicator_name] = (source_name, implementation)

    # a new price bar has arrived
    # that will trigger operatotion of moving through all the indicators
    # passing values in and calculating outcomes
    def new_price_bar(self, price_bar):

        if price_bar is None:
            raise ValueError("price_bar is null")

        self.__update_static_values(price_bar)

        # move through all listed indicators and calculate all of those
        for indicator_name, indicator_record in self.__all_indicators.iteritems():

            source_name, indicator = indicator_record
            if source_name is not None:
                current_value_at_source = self[source_name]

                indicator.on_new_upstream_value(current_value_at_source)

    # update values related to static fields, mainly: price bar fields
    def __update_static_values(self, price_bar):
        field_values = {"open": price_bar.open, "close": price_bar.close,
                        "high": price_bar.high, "low": price_bar.low,
                        "volume": price_bar.volume,
                        "trade_buy": None, "trade_sell": None, "trade_short": None}

        for key, value in field_values.iteritems():
            # these are all static values, so the only impact here is recording new values
            source_name, indicator = self.__all_indicators[key]
            indicator.on_new_upstream_value(value)

    # get all values for the given indicator
    def get_all_values_for_indicator(self, indicator_name):
        source_name, indicator = self.__all_indicators[indicator_name]

        return indicator.all_result

    @property
    def indicator_names(self):
        # return names of all collected indicators
        return self.__all_indicators.keys()

    # mark one of the transaction indicator (buy, sell or short) with the given value
    # (which in most cases will be current price)
    def mark_transaction(self, transaction_name, mark_value):
        transaction_indicator_name = self.TRANSACTION_TO_FIELD_NAME[transaction_name]

        source_indicator, indicator = self.__all_indicators[transaction_indicator_name]

        # update existing static value indicator, but check if it's actually not-set
        # if it's set with some value already, we have some issue with the logic
        if indicator.all_result[-1] is not None:
            raise Exception('There''s some value, but None is expected!!!')

        indicator.all_result[-1] = mark_value

    # get current value for the indicator name
    def __getitem__(self, indicator_name):
        source_name, indicator = self.__all_indicators[indicator_name]

        return indicator.result
