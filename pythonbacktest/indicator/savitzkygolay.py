from .base import AbstractIndicator
from scipy.signal import savgol_filter


class SavitzkyGolay(AbstractIndicator):

    def __init__(self, indicator_name, window_size, polyorder,
                 level=1, calculate_buffer_size=-1,
                 keep_last_results_only=True,
                 source_indicators=None):
        """
        Constructor
        :param window_size: Windows size
        :param polyorder: Polyorder
        :param level: How many times Savitzky-Golay should be run on the given set of data. 1 by default.
        :param calculate_buffer_size: If set, SavGol will be calculated on last 'calculate_buffer_size'
               or 'window_size' elements in the buffer - whichever is larger
        :param keep_last_results_only: For each new record comming calculate savgol, then: take last result from
                __all_results and save it to __last_results
                WARNING: this will work only when this indicator consumes
                only the latest result from the upstream indicator
        """
        AbstractIndicator.__init__(self, indicator_name, source_indicators)

        self.__window_size = window_size
        self.__polyorder = polyorder
        self.__calculate_buffer_size = calculate_buffer_size
        self.__keep_last_results_only = keep_last_results_only

        if level < 1:
            raise ValueError("level cannot be less than 1")

        self.__level = level

        self.reset()

    def reset(self):
        self.__data_storage = []
        self.__temp_all_results = []
        self.__last_results = []

    @property
    def result(self):
        return self.__temp_all_results[-1]

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()

        if new_value is None:
            self.add_new_result(None)
            return

        self.__data_storage.append(new_value)
        self.__calculate_results()

    def __calculate_results(self):

        none_count = 0
        self.__temp_all_results = []

        # count leading Nones and add them to the result
        for element in self.__data_storage:
            if element is not None:
                break
            none_count += 1
            self.__temp_all_results.append(None)

        # set temp_storage to non-none elements only
        temp_storage = self.__data_storage[none_count:]

        window_size = self.__window_size
        calculate_buffer_size = self.__calculate_buffer_size

        if len(temp_storage) >= window_size:
            passive_data = []
            if len(temp_storage) >= calculate_buffer_size > 0:
                passive_data = temp_storage[:-calculate_buffer_size]
                temp_storage = temp_storage[-calculate_buffer_size:]

            # depending on the level calculate Savgol multiple times recursively
            for level_count in range(0, self.__level):
                temp_storage = savgol_filter(temp_storage, window_size, self.__polyorder).tolist()

            self.__temp_all_results.extend(passive_data)
            self.__temp_all_results.extend(temp_storage)
        else:
            self.__temp_all_results.extend([None] * len(temp_storage))

        # lets store the latest result
        if self.__keep_last_results_only:
            self.add_new_result(self.__temp_all_results[-1])
        else:
            self.set_all_results(self.__temp_all_results)


