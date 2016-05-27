from .abstractindicator import AbstractIndicator

class DataProcessor(AbstractIndicator):

    def __init__(self, processing_proc):
        self.__current_value = None
        self.__all_values = []
        self.__all_results = []

        if processing_proc is None:
            raise ValueError("processing_proc must be set")

        self.__processing_proc = processing_proc

    @property
    def result(self):
        return self.__all_results[-1]

    @property
    def all_result(self):
        return self.__all_results

    def on_new_upstream_value(self, new_value):

        if new_value is None:
            self.__all_values.append(None)
        else:
            if type(new_value) is list:
                del self.__all_values[:(len(new_value) - 1)]
                self.__all_values.extend(new_value)
            else:
                self.__all_values.append(new_value)

            # ... and recalculate entire data on processing function
            self.__process_all_values()

    def __process_all_values(self):
        self.__all_results = []

        for value in self.__all_values:
            single_result = self.__processing_proc(value)
            self.__all_results.append(single_result)
