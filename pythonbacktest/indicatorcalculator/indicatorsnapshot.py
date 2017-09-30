# this class is responsible for keeping snapshot of the current status of the Indicators
class IndicatorsSnapshot(object):

    def __init__(self, timestamp):
        # dictionary keeping status of indicators at the given moment in time, structure:
        # - key - name of the indicator
        # - value - list of values of the indicator at to this moment in time for the given day
        self.__snapshot_data = {}

        # Data transformed into list of dictionaries
        # as oppose to dictionary as list (the default set-up): __snapshot_data
        # This value is set after first reference
        self.__snapshot_data_list = []

        self.___snapshots_timestamp = timestamp

        self.__records_length = 0

    def save_indicator_snapshot(self, timestamp, indicator_name, all_indicator_values):

        # consistency check - saved indicator values must be on the same timestamp
        if timestamp != self.___snapshots_timestamp:
            raise ValueError("Indicator snapshot has invalid timestamp. Expected %s, got: %s"
                             % (str(self.___snapshots_timestamp), str(timestamp)))

        # check of there're data already saved for this indicator name
        if indicator_name in self.__snapshot_data:
            raise ValueError("There's already snapshot data for indicator: %s, timestamp: %s"
                             % (indicator_name, str(timestamp)))

        if not self.__snapshot_data:
            self.__records_length = len(all_indicator_values)
        else:
            new_data_lenght = len(all_indicator_values)
            if self.__records_length != new_data_lenght:
                raise ValueError(f"Wrong length of the indicator values. Expected: {self.__records_length}, "
                                 f"got {new_data_lenght}")

        self.__snapshot_data[indicator_name] = list(all_indicator_values)

    @property
    def snapshot_data(self):
        return self.__snapshot_data

    @property
    def snapshot_data_list(self):
        """
        Return data transformed into list of dictionaries
        as oppose to dictionary as list (the default set-up)
        :return:
        """
        self.__calculate_snapshot_data_list()
        return self.__snapshot_data_list

    def __calculate_snapshot_data_list(self):
        if not self.__snapshot_data_list and self.__snapshot_data:
            self.__snapshot_data_list = []

            indicator_names = list(self.__snapshot_data.keys())
            indicator_values_all = iter(zip(*self.__snapshot_data.values()))

            for indicator_values in indicator_values_all:
                self.__snapshot_data_list.append(dict(zip(indicator_names, indicator_values)))


