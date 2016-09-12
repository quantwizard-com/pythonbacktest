from pythonbacktest.datafeed import PriceBar
from . import *


class BasicBackTestEngine(AbstractBackTestEngine):

    def __init__(self):
        AbstractBackTestEngine.__init__(self)

    # run backtest on single day only
    def start_single_date(self, date, strategy, indicators_history, broker):

        indicators_history_per_date = indicators_history.get_indicator_history_for_day(date)

        if indicators_history_per_date is None:
            raise ValueError("Can't get history for given date: " + str(date))

        price_bar_index = 0

        for timestamp, indicators_snapshot in indicators_history_per_date:
            snapshot_data = indicators_snapshot.snapshot_data
            latest_snapshot_data = self.__get_latest_values_for_indicators_snapshot(snapshot_data)
            price_bar = self.__latest_snapshot_to_price_bar(latest_snapshot_data)

            broker.set_current_price_bar(price_bar, price_bar_index)
            strategy.new_price_bar(price_bar, snapshot_data, latest_snapshot_data, broker)
            price_bar_index += 1

    def __get_latest_values_for_indicators_snapshot(self, snapshot_data):
        result = {}

        for indicator_name, indicator_values in snapshot_data.iteritems():
            result[indicator_name] = indicator_values[-1]

        return result

    def __latest_snapshot_to_price_bar(self, latest_snapshot_data):
        price_bar = PriceBar()
        price_bar.timestamp = latest_snapshot_data["timestamp"]
        price_bar.open = latest_snapshot_data["open"]
        price_bar.close = latest_snapshot_data["close"]
        price_bar.high = latest_snapshot_data["high"]
        price_bar.low = latest_snapshot_data["low"]
        price_bar.volume = latest_snapshot_data["volume"]

        return price_bar


