from abc import ABC, abstractmethod
import numpy as np


class AbstractIndicator(ABC):

    def __init__(self, indicator_name, source_indicators=None):

        self.__indicator_name = indicator_name

        if not indicator_name:
            raise ValueError("Indicator name has to be set.")

        # collection of the source indicators specs; each items can be defined in 2 forms
        # - reference to the source indicator
        # - (reference, string) - some indicators can have multiple-data for each result, so additional
        #                         string value will point on exact name of the result
        self.__source_indicators_specs = []

        self.set_source_indicators(source_indicators)

        # these are results of the indicator calculations on the time scale
        # meaning: for each single input record there's single result record
        self.__all_indicator_results = np.array()

        super().__init__()

    def reset(self):
        """
        Reset indicator to the initial value. It's called when IndicatorsCalculator
        starts calculation for single date
        :return: None
        """
        self.__all_indicator_results = np.array()

    def set_source_indicators(self, source_indicators):
        """
        Set indicators (1 or more, which data will be consumed from.
        :param source_indicators: List of the source indicators
        """
        self.__source_indicators_specs = None

        if not source_indicators:
            return

        if source_indicators is not None:
            if isinstance(source_indicators, list):
                self.__source_indicators_specs = source_indicators
            else:
                self.__source_indicators_specs = [source_indicators]

    @property
    def indicator_name(self):
        return self.__indicator_name

    @property
    def latest_result(self):
        """
        get LATEST indicator value (as: latest value);
        this should be called ONLY if results consist of single values;
        :return: LATEST indicator value
        """
        return self.get_latest_result(None)

    def get_latest_result(self, string_reference=None):
        """
        Get latest result as specified by the string reference
        :param string_reference:
        :return: LATEST indicator value pointed by the string reference
        """
        indicator_results = self.all_results
        if not indicator_results:
            return None

        indicator_result_record = indicator_results[-1]

        if type(indicator_result_record) is dict:
            if string_reference is None:
                # if there's no reference to the particular part of the indicator,
                # then return entire dictionary
                # it's up to requestor to handle this
                return indicator_result_record

            if string_reference not in indicator_result_record:
                raise ValueError("string_reference not recognized")

            # complex dict record
            return indicator_result_record[string_reference]
        else:
            if string_reference is not None:
                raise ValueError(f"string_reference is specified as '{string_reference}', "
                                 f"but indicator has simple results only.")

            # simple value record
            return indicator_result_record

    @property
    def all_results(self):
        """
        return entire collection of results for the given indicator
        e.g.: for SMA that would be all SMA values for the given input
        :return: All indicator results
        """
        return self.__all_indicator_results

    def add_new_result(self, new_result):
        """
        Add new single result to the collection
        """
        self.__all_indicator_results.append(new_result)

    def set_all_results(self, results):
        """
        Force setting of all results
        :param results: Results to be set
        """
        self.__all_indicator_results = results

    def get_latest_data_from_source_indicators(self):
        """
        Download latest records from the source indicators based on the __source_indicators variable
        Return single value - if there's single source indicator spec
        or collection - if 2 or more specs
        :return:
        """
        source_indicators_data = []

        source_indicator_specs = self.__source_indicators_specs

        if not source_indicator_specs:
            raise ValueError(f'Source indicator specs not set. Indicator name: {self.indicator_name}')

        for source_indicator_spec in self.__source_indicators_specs:
            string_reference = None

            if type(source_indicator_spec) is tuple:
                indicator_reference, string_reference = source_indicator_spec
            else:
                indicator_reference = source_indicator_spec

            source_indicators_data.append(indicator_reference.get_latest_result(string_reference))

        if len(source_indicators_data) >= 2:
            return tuple(source_indicators_data)
        else:
            return source_indicators_data[0]

    @property
    def source_indicators(self):
        return self.__source_indicators_specs

    def new_upstream_record(self):
        """
        We've got a new data record in the upstream source indicator
        """
        previous_results_count = len(self.all_results)

        # process new record
        self._process_new_upstream_record()

        # there should be exactly one new record in the result
        new_results_count = len(self.__all_indicator_results) - previous_results_count

        if new_results_count != 1:
            raise ValueError(f"{self.indicator_name}: Expected 1 new result, got {new_results_count} instead.")

    @abstractmethod
    def _process_new_upstream_record(self):
        """
        This method should be implemented in the derived class
        """
        raise NotImplementedError()
