from pythonbacktest.indicator import IndicatorHistory
from pythonbacktest.indicator import IndicatorsSnapshot
from .staticvalue import StaticValue
from collections import OrderedDict
import copy


class IndicatorsCalculator(object):

    ALL_STATIC_INDICATORS = ["timestamp", "open", "close", "high", "low", "volume"]

    def __init__(self):
        """
        Constructor with copying functionality
        :type indicators_to_copy: Indicators
        """
        self.__all_indicators = OrderedDict()

        # counter which checks how many price bars in total have been processed at the indicators
        # number of processed bars should be consistent with number of results per each indicator
        # so this counter is used primarily to check on how individual indicators behave
        self.__price_bars_counter = 0

        # set static values for price bar values
        for price_bar_field in self.ALL_STATIC_INDICATORS:
            self.__all_indicators[price_bar_field] = {'source': None, 'implementation': StaticValue(),
                                                      'passalldata': False}

    # indicators - define collection of indicators, which should be collected during trading;
    #   collection of dictionaries with following fields:
    # - name - indicator name
    # - source name - name of the indicator, which should be an input for the given indicator
    # - implementation - implementation of the indicator
    # - datacount - if specified, source data will be extracted from 'source name' from all_result;
    #               it will extract 'datacount' last records
    def define_indicators_map(self, indicator_records):

        for record in indicator_records:

            indicator_name = record['name']
            source_name = record['source']
            implementation = record['implementation']
            if 'passalldata' not in record:
                record['passalldata'] = False

            if indicator_name in self.__all_indicators.iteritems():
                raise ValueError("Indicator with name '%s' is already declared" % indicator_name)

            if source_name is None or implementation is None:
                raise ValueError("Either input_name or implementation is null")

            self.__all_indicators[indicator_name] = record

    def run_computation(self, date, data_feed):

        # make sure all indicator implementations are 'clear'
        self.__reset_all_implementations()

        # let's extract single date and test price bars for that date
        price_bars_per_date = data_feed.get_prices_bars_for_day(date)

        if price_bars_per_date is None:
            raise "Can't extract data for date: " + date

        indicators_history = IndicatorHistory()

        for price_bar in price_bars_per_date:
            # calculate status of the indicators, get snapshot and save it to the history
            indicator_snapshot = self.__new_price_bar(price_bar)
            indicators_history.store_snapshot(price_bar.timestamp, indicator_snapshot)

        return indicators_history

    # a new price bar has arrived
    # that will trigger operatotion of moving through all the indicators
    # passing values in and calculating outcomes
    def __new_price_bar(self, price_bar):

        if price_bar is None:
            raise ValueError("price_bar is null")

        self.__price_bars_counter += 1
        self.__update_static_indicators(price_bar)
        timestamp = price_bar.timestamp

        indicators_snapshot = IndicatorsSnapshot(timestamp)

        # move through all listed indicators and calculate all of those
        for indicator_name, indicator_record in self.__all_indicators.iteritems():

            implementation = indicator_record['implementation']
            passalldata = indicator_record['passalldata']
            source_indicator_names = indicator_record['source']
            if source_indicator_names is not None:

                if passalldata:
                    all_results_from_source = self.__get_all_results(source_indicator_names)
                    implementation.on_new_upstream_value(*all_results_from_source)
                    passed_data = all_results_from_source
                else:
                    current_value_at_source = self.__get_result(source_indicator_names)
                    implementation.on_new_upstream_value(*current_value_at_source)
                    passed_data = current_value_at_source

                # once indicator is updated, number of results
                all_results_count = len(implementation.all_result)

                # self-check: number of results on the Indicator MUST BE the same as number of pricebars
                # passed to this method; this is important to align all indicators with price bars
                if all_results_count != self.__price_bars_counter:
                    raise ValueError("Indicator: %s, expected: %d records, actual: %d, passed data: %s"
                                     % (indicator_name, self.__price_bars_counter, all_results_count, passed_data))

            indicators_snapshot.save_indicator_snapshot(timestamp, indicator_name, implementation.all_result)

        return indicators_snapshot

    # update values related to static fields, mainly: price bar fields
    def __update_static_indicators(self, price_bar):
        field_values = {"timestamp": price_bar.timestamp,
                        "open": price_bar.open, "close": price_bar.close,
                        "high": price_bar.high, "low": price_bar.low,
                        "volume": price_bar.volume}

        for key, value in field_values.iteritems():
            # these are all static values, so the only impact here is recording new values
            implementation = self.__all_indicators[key]['implementation']
            implementation.on_new_upstream_value(value)

    # get all values for the given indicator
    def get_all_values_for_indicator(self, indicator_name):
        implementation = self.__all_indicators[indicator_name]['implementation']

        return implementation.all_result

    @property
    def indicator_names(self):
        # return names of all collected indicators
        return self.__all_indicators.keys()

    # get current value for the indicator name
    def __getitem__(self, indicator_name):
        implementation = self.__all_indicators[indicator_name]['implementation']

        return implementation.result

    def __get_all_results(self, indicator_names):

        all_source_results = []
        all_source_indicator_names = indicator_names if type(indicator_names) is list else [indicator_names]

        for indicator_name in all_source_indicator_names:
            implementation = self.__all_indicators[indicator_name]['implementation']
            all_source_results.append(implementation.all_result)

        return all_source_results

    def __get_result(self, indicator_names):

        source_results = []
        source_indicator_names = indicator_names if type(indicator_names) is list else [indicator_names]

        for indicator_name in source_indicator_names:
            implementation = self.__all_indicators[indicator_name]['implementation']
            source_results.append(implementation.result)

        return source_results

    def __reset_all_implementations(self):
        for indicator_name, indicator_record in self.__all_indicators.iteritems():
            indicator_record['implementation'].reset()
