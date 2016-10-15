from . import AbstractIndicator
from Queue import Queue


# delay input data by the given number of cycles
class DataDelay(AbstractIndicator):

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
            self.__initiate_data()

            for number in new_value:
                self.__add_number_to_queue(number)
        else:
            self.__add_number_to_queue(new_value)

    def __add_number_to_queue(self, number):

        self.__delay_queue.put(number)

        result = None
        if self.__delay_queue.qsize() > self.__delay_size:
            result = self.__delay_queue.get()

        self.__latest_result = result
        self.__all_results.append(result)

    def __initiate_data(self):
        self.__delay_queue = Queue(maxsize=0)

        self.__latest_result = None
        self.__all_results = []


