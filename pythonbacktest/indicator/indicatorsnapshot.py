import copy


# this class is responsible for keeping snapshot of the current status of the Indicators
class IndicatorsSnapshot(object):

    def __init__(self, timestamp, indicators):
        # dictionary keeping status of indicators at the given moment in time, structure:
        # - key - name of the indicators
        # - value - list of values of the indicator at to this moment in time for the given day
        self.__snapshot_data = {}

        # first - take names of all indicators
        indicator_names = indicators.indicator_names

        for name in indicator_names:
            all_values_for_indicator = indicators.get_all_values_for_indicator(name)
            self.__snapshot_data[name] = copy.copy(all_values_for_indicator)

        # when the snapshot was taken
        self.__snapshot_timestamp = timestamp

    @property
    def snapshot_data(self):
        return self.__snapshot_data

