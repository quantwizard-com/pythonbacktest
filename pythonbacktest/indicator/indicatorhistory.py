from indicators import Indicators


# collection of indicators for given moment in day and time
# prime purpose: checking status of the individual indicators
# at the time of trading; this is due the fact that some of the indicators
# may not have the same state at the particular time when looking from
# current and future time points, so it's important to understand
# where things were at the time of trade
class IndicatorHistory(object):

    def __init__(self):

        # dictonary of dictionaries storing information about indicators
        # - key - date of trade
        # - value - dictionary: indicators for all data points during that day
        # -- key - date and time of indicators
        # -- value - Indicators object with all collected indicators
        self.__indicators_storage = {}

    def record_state_of_indicators(self, timestamp, indicators):
        """
        record single snapshot of all indicators for the given timestamp parameters
        :param timestamp: date and time of when indicators were recorded
        :param indicators: Indicators object implementation; status of the indicators at the given timestamp
        """

        date = timestamp.date()

        if date not in self.__indicators_storage:
            self.__indicators_storage[date] = {}
        elif timestamp in self.__indicators_storage[date]:
            raise ValueError("Duplicated indicators for timestamp: " + str(timestamp))

        # ok, ready to insert indicators
        copy_of_indicators = Indicators(indicators)
        self.__indicators_storage[date][timestamp] = copy_of_indicators
