from .base import AbstractIndicator

class DataCrossIndicator(AbstractIndicator):
    """
    Indicator detecting if there was cross between 2 series of the data
    Cross: meaning that data from s1 wa below s2 and then in next data point is above s2,
        then the output result for that point is 1, else: 0
    """

    def __init__(self, indicator_name, source_indicators=None):
        AbstractIndicator.__init__(self,
                                   indicator_name=indicator_name,
                                   source_indicators=source_indicators)
        self.reset()

    def reset(self):
        AbstractIndicator.reset(self)
        self.__previous_s1 = None
        self.__previous_s2 = None

    def _process_new_upstream_record(self):
        value1, value2 = self.get_latest_data_from_source_indicators()

        p1 = self.__previous_s1
        p2 = self.__previous_s2

        result = 0
        if p1 and p2:
            if p1 < p2 and value1 > value2 or \
                p1 > p2 and value1 < value2:
                    result = 1

        self.__previous_s1 = value1
        self.__previous_s2 = value2

        self.all_results.append(result)
