from pythonbacktest.indicatorcalculator import IndicatorsSnapshot
from pythonbacktest.indicator.staticvalue import StaticValue
from collections import OrderedDict
from .indicatorsmapindicatorrecord import IndicatorsMapIndicatorRecord
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

            implementation = indicator_record.implementation
            source_indicator_names = indicator_record['source']

            if source_indicator_names is not None:

                passed_data = self.__get_result(source_indicator_names)

                # pass data to downstream
                execution_start_time = time.time()
                implementation.on_new_upstream_value(*passed_data)
                if self.__performance_monitor:
                    self.__performance_monitor.report_execution_time(indicator_name, time.time() - execution_start_time)

            self.__assert_all_results_count(implementation.all_result, indicator_name, passed_data)

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
        return list(self.__all_indicators.keys())

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

    def __assert_all_results_count(self, all_results, indicator_name, passed_data):

        # once indicator is updated, number of results
        all_results_count = len(all_results)

        # self-check: number of results on the Indicator MUST BE the same as number of pricebars
        # passed to this method; this is important to align all indicators with price bars
        if all_results_count != self.__price_bars_counter:
            raise ValueError("Indicator: %s, expected: %d records, actual: %d, passed data: %s"
                             % (indicator_name, self.__price_bars_counter, all_results_count, passed_data))

    def __find_source_indicators(self, source_indicators_name):

        if isinstance(source_indicators_name, list):
            return list(map(lambda name: self.__all_indicators[name], source_indicators_name))
        else:
            return [self.__all_indicators[source_indicators_name]]

