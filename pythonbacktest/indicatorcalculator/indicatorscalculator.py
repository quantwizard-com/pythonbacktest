from pythonbacktest.indicatorcalculator import IndicatorsSnapshot
from pythonbacktest.indicator.staticvalue import StaticValue
from collections import OrderedDict
import time


class IndicatorsCalculator(object):

    ALL_STATIC_INDICATORS = ["timestamp", "open", "close", "high", "low", "volume"]

    def __init__(self, performance_monitor=None):
        """
        Constructor with copying functionality
        :type indicators_to_copy: Indicators
        """
        self.__all_indicators = OrderedDict()

        # counter which checks how many price bars in total have been processed at the indicators
        # number of processed bars should be consistent with number of results per each indicator
        # so this counter is used primarily to check on how individual indicators behave
        self.__price_bars_counter = 0

        self.__performance_monitor = performance_monitor

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

            if indicator_name in self.__all_indicators.items():
                raise ValueError("Indicator with name '%s' is already declared" % indicator_name)

            if source_name is None or implementation is None:
                raise ValueError("Either input_name or implementation is null")

            self.__all_indicators[indicator_name] = record

    def reset(self):
        self.__reset_all_implementations()

    # a new price bar has arrived
    # that will trigger operation of moving through all the indicators
    # passing values in and calculating outcomes
    def new_price_bar(self, price_bar):

        if price_bar is None:
            raise ValueError("price_bar is null")

        self.__price_bars_counter += 1
        self.__update_static_indicators(price_bar)
        timestamp = price_bar.timestamp

        indicators_snapshot = IndicatorsSnapshot(timestamp)

        # move through all listed indicators and calculate all of those
        for indicator_name, indicator_record in self.__all_indicators.items():

            implementation = indicator_record['implementation']
            passalldata = indicator_record['passalldata']
            source_indicator_names = indicator_record['source']
            if source_indicator_names is not None:

                # get data from up-stream
                if passalldata:
                    passed_data = self.__get_all_results(source_indicator_names)
                else:
                    passed_data = self.__get_result(source_indicator_names)

                # pass data to downstream
                execution_start_time = time.time()
                implementation.on_new_upstream_value(*passed_data)
                if self.__performance_monitor:
                    self.__performance_monitor.report_execution_time(indicator_name, time.time() - execution_start_time)

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

        # these are all static values, so the only impact here is recording new values
        self.__all_indicators["timestamp"]['implementation'].on_new_upstream_value(price_bar.timestamp)
        self.__all_indicators["open"]['implementation'].on_new_upstream_value(price_bar.open)
        self.__all_indicators["close"]['implementation'].on_new_upstream_value(price_bar.close)
        self.__all_indicators["high"]['implementation'].on_new_upstream_value(price_bar.high)
        self.__all_indicators["low"]['implementation'].on_new_upstream_value(price_bar.low)
        self.__all_indicators["volume"]['implementation'].on_new_upstream_value(price_bar.volume)

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
        for indicator_name, indicator_record in self.__all_indicators.items():
            indicator_record['implementation'].reset()
