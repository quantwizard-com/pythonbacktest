import numpy as np

class IndicatorsCalculatorPerfMonitor(object):

    def __init__(self):
        self.__performance_data = {}

    def report_execution_time(self, indicator_name, execution_time):

        if indicator_name in self.__performance_data:
            self.__performance_data[indicator_name].append(execution_time)
        else:
            self.__performance_data[indicator_name] = [execution_time]

    @property
    def performance_stats(self):
        for key, value in self.__performance_data.items():
            yield key, (np.mean(value), np.min(value), np.max(value), np.median(value), np.std(value))

    @property
    def performance_data(self):
        return self.__performance_data