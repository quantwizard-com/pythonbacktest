import abc


class AbstractIndicator(object):

    def __init__(self, source_indicators):
        self.__source_indicators = []
        self.set_source_indicators(source_indicators)

        # these are results of the indicator calculations on the time scale
        # meaning: for each single input record there's single result record
        self.__all_indicator_results = []

    @abc.abstractmethod
    def reset(self):
        """
        Reset indicator to the initial value. It's called when IndicatorsCalculator
        starts calculation for single date
        :return: None
        """
        self.__all_indicator_results = []

    def set_source_indicators(self, source_indicators):
        """
        Set indicators (1 or more, which data will be consumed from.
        :param source_indicators: List of the source indicators
        """
        self.__source_indicators = None

        if source_indicators is not None:
            if isinstance(source_indicators, list):
                self.__source_indicators = source_indicators
            else:
                self.__source_indicators = [list]

    @property
    def latest_result(self):
        """
        get LATEST indicator value (as: latest value)
        :return: LATEST indicator value
        """
        indicator_results = self.__all_indicator_results
        if indicator_results:
            return indicator_results[-1]
        else:
            return None

    @property
    def all_results(self):
        """
        return entire collection of results for the given indicator
        e.g.: for SMA that would be all SMA values for the given input
        :return: All indicator results
        """
        return self.__all_indicator_results

    @property
    def source_indicators(self):
        return self.__source_indicators

    def new_upstream_record(self):
        """
        We've got a new data record in the upstream source indicator
        """
        previous_results_count = len(self.__all_indicator_results)
        self.__process_new_upstream_record()

        # there should be exactly one new record in the result
        new_results_count = len(self.__all_indicator_results) - previous_results_count

        if new_results_count != 1:
            raise ValueError(f"Expected 1 new result, got {new_results_count} instead.")

    @abc.abstractmethod
    def __process_new_upstream_record(self):
        """
        This method should be implemented in the derived class
        """
        raise NotImplementedError()