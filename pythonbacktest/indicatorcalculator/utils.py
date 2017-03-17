import numpy as np
import datetime

class Utils(object):

    def get_list_from_last_snapshot_per_day(self, indicators_history, snapshot_date, indicator_name):
        '''
        Get last snapshot from the indicators history for the given indicator name
        and turn that data into list
        :param snapshot_date:
        :return:
        '''
        indicators_snapshot = indicators_history.get_last_indicator_snapshot_per_day(snapshot_date)

        return indicators_snapshot.snapshot_data[indicator_name]

    def calculate_indicator_sigmas(self, indicators_history, snapshot_date):
        '''
        Return dictionary with name of indicators, with list of tuples (values of sigmas 1-5 and percentage of values falling into those)
        :param indicator_history:
        :param snapshot_date:
        :return:
        '''

        result = {}
        SIGMAS_RANGE = range(1, 6)

        indicators_snapshot = indicators_history[snapshot_date].get_last_indicator_snapshot_per_day(snapshot_date)

        for indicator_name, unfiltered_values in indicators_snapshot.snapshot_data.items():

            values = list(filter(lambda x: x is not None, unfiltered_values))

            if type(values[0]) is not datetime.datetime:
                std = np.std(values)
                mean = np.mean(values)

                sigmas_result = {}

                for sigma in SIGMAS_RANGE:
                    sigma_value_plus = mean + std * sigma
                    sigma_value_minus = mean - std * sigma

                    percentage_in_range = sum(sigma_value_minus <= i <= sigma_value_plus for i in values) * 100.0 / len(values)

                    sigmas_result[sigma] = ((sigma_value_minus, sigma_value_plus), percentage_in_range)

                result[indicator_name] = mean, sigmas_result

        return result




