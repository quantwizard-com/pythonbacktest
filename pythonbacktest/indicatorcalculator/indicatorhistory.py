from collections import OrderedDict


# collection of indicator snapshots for given moment in day and time
# prime purpose: checking status of the individual indicators
# at the time of trading; this is due the fact that some of the indicators
# may not have the same state at the particular time when looking from
# current and future time points, so it's important to understand
# where things were at the time of trade
class IndicatorHistory(object):

    def __init__(self):

        # dictonary of dictionaries storing snapshots of the indicators
        # - key - date of the price bars and indicators
        # - value - dictionary: indicators for all data points during that day
        # -- key - date and time of indicators
        # -- value - IndicatorsSnapshot object with all collected indicators
        self.__indicators_storage = OrderedDict()

    def store_snapshot(self, timestamp, indicators_snapshot):
        date = timestamp.date()

        if date not in self.__indicators_storage:
            self.__indicators_storage[date] = OrderedDict()

        if timestamp in self.__indicators_storage[date]:
            raise ValueError("Duplicated indicators for timestamp: " + str(timestamp))

        # ok, time to copy indicators into a snapshot
        self.__indicators_storage[date][timestamp] = indicators_snapshot

    # return sorted list of tuples (sorted by datetime)
    # value 1: date time of when the indicator has been recorded
    # value 2: actual snapshot of the Indicators object
    # e.g.: [(2016-01-02 14:30.00, IndicatorsSnapshot),(2016-01-02 14:30.05, IndicatorsSnapshot)]
    def get_indicator_history_for_day(self, day_date):
        data_per_day = self.__indicators_storage[day_date]

        # return list of key, values, where: key is datetime and value: all collected indicators for that timestamp
        return data_per_day.items()

    # get last snapshot of all recorded indicators for the given day
    def get_last_indicator_snapshot_per_day(self, day_date):
        data_per_day = self.__indicators_storage[day_date]
        last_key = list(data_per_day.keys())[-1]

        return data_per_day[last_key]

    @property
    def all_indicator_names(self):
        """
        Return names of all stored indicators
        """
        return self.__indicator_names

