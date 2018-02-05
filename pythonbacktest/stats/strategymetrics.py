import numpy as np


class StrategyMetrics(object):

    @staticmethod
    def sharpe(input_data, benchmark = 0):
        n = len(input_data)

        return np.sqrt(n) * (np.mean(input_data) - benchmark) / (np.std(input_data))
