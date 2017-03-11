from . import AbstractIndicator
from scipy.signal import savgol_filter


class SavitzkyGolay(AbstractIndicator):

    def __init__(self, window_size, polyorder, level=1, calculate_buffer_size=-1):
        """
        Constructor
        :param window_size: Windows size
        :param polyorder: Polyorder
        :param level: How many times Savitzky-Golay should be run on the given set of data. 1 by default.
        :param calculate_buffer_size: If set, SavGol will be calculated on last 'calculate_buffer_size'
               or 'window_size' elements in the buffer - whichever is larger
        """
        AbstractIndicator.__init__(self)

        self.__window_size = window_size
        self.__polyorder = polyorder
        self.__calculate_buffer_size = calculate_buffer_size

        if level < 1:
            raise ValueError("level cannot be less than 1")

        self.__level = level

        self.reset()

    def reset(self):
        self.__data_storage = []
        self.__all_results = []

    @property
    def all_result(self):
        return self.__all_results

    @property
    def result(self):
        return self.__all_results[-1]

    def on_new_upstream_value(self, new_value):

        # we expect None or array of numbers, which has exactly 'window_size' elements
        if new_value is None:
            self.__data_storage.append(None)
        else:
            if type(new_value) is not list:
                new_value = [new_value]

            # the assumption is we have only one additional value
            # all the others is overwriting old (n-1) values
            if len(new_value) > 1:
                del self.__data_storage[:(len(new_value) - 1)]

            self.__data_storage.extend(new_value)

            self.__calculate_results()

    def __calculate_results(self):

        none_count = 0
        self.__all_results = []

        # count leading Nones and add them to the result
        for element in self.__data_storage:
            if element is None:
                none_count += 1
                self.__all_results.append(None)
            else:
                break

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

            self.__all_results.extend(passive_data)
            self.__all_results.extend(temp_storage)
        else:
            self.__all_results.extend([None] * len(temp_storage))


