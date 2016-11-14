from pythonbacktest.indicatorcalculator import IndicatorHistory


class BacktestIndicatorsCalculator(object):
    """
    Class responsible for generating Indicators History for given collection of the input data feed (price bars)
    """

    def run_computation(self, date, data_feed, indicators_calculator):
        """
        Run computation of the target Indicators Calculator based on the input data feed
        :param date: Date to be run computation on (assumption is that data_feed contains data for that day)
        :param data_feed: Data storage with the price bars
        :param indicators_calculator: Calculator keeping state of the indicators after each new price bar
        :return:
        """

        # make sure all indicator implementations are 'clear'
        indicators_calculator.reset()

        # let's extract single date and test price bars for that date
        price_bars_per_date = data_feed.get_prices_bars_for_day(date)

        if price_bars_per_date is None:
            raise "Can't extract data for date: " + date

        indicators_history = IndicatorHistory()

        for price_bar in price_bars_per_date:
            # calculate status of the indicators, get snapshot and save it to the history
            indicator_snapshot = indicators_calculator.new_price_bar(price_bar)
            indicators_history.store_snapshot(price_bar.timestamp, indicator_snapshot)

        return indicators_history
