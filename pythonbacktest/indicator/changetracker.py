from . import *
import queue as queue


class ChangeTracker(AbstractIndicator):
    """
    This indicator does 2 things:
    - delays given data stream by given period
    - calculates difference between main data stream and the delayed one
    As such this is combination of DataDelay and DataDifference indicators chained together
    """

    def __init__(self, delay_size):
        AbstractIndicator.__init__(self)

        self.__delay_size = delay_size
        self.reset()

    def reset(self):
        self.__initiate_data()

    @property
    def result(self):
        return self.__latest_result

    @property
    def all_result(self):
        return self.__all_results

    def on_new_upstream_value(self, new_value):

        if type(new_value) is list:
            raise ValueError("Lists are not supported as an input value")
        else:
            self.__add_number_to_queue(new_value)

    def __add_number_to_queue(self, number):

        self.__delay_queue.put(number)

        result = None
        if self.__delay_queue.qsize() > self.__delay_size:
            delayed_number = self.__delay_queue.get()
            result = None if delayed_number is None else number - delayed_number

        self.__latest_result = result
        self.__all_results.append(result)

    def __initiate_data(self):
        self.__delay_queue = queue.Queue(maxsize=0)

        self.__latest_result = None
        self.__all_results = []


