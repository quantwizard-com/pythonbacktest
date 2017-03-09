# this class is responsible for keeping snapshot of the current status of the Indicators
class IndicatorsSnapshot(object):

    def __init__(self, timestamp):
        # dictionary keeping status of indicators at the given moment in time, structure:
        # - key - name of the indicator
        # - value - list of values of the indicator at to this moment in time for the given day
        self.__snapshot_data = {}

        self.___snapshots_timestamp = timestamp

    def save_indicator_snapshot(self, timestamp, indicator_name, all_indicator_values):

        # consistency check - saved indicator values must be on the same timestamp
        if timestamp != self.___snapshots_timestamp:
            raise ValueError("Indicator snapshot has invalid timestamp. Expected %s, got: %s"
                             % (str(self.___snapshots_timestamp), str(timestamp)))

        # check of there're data already saved for this indicator name
        if indicator_name in self.__snapshot_data:
            raise ValueError("There's already snapshot data for indicator: %s, timestamp: %s"
                             % (indicator_name, str(timestamp)))

        self.__snapshot_data[indicator_name] = list(all_indicator_values)

    @property
    def snapshot_data(self):
        return self.__snapshot_data

