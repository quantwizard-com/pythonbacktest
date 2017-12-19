import abc

from pythonbacktest.ai.backoffice.tradehistory import TradeHistory
from pythonbacktest.visualization import AbstractDataVisualization
from pythonbacktest.indicatorshistory import IndicatorHistory


class AbstractChartRenderer(AbstractDataVisualization):

    def __init__(self, width=900, height=500):
        AbstractDataVisualization.__init__(self)

        self.__chart_width = width
        self.__chart_height = height

    def render_charts(self, indicators_history, *indicators_to_display):
        per_chart_data = self.__get_indicators_data_per_chart(indicators_history, indicators_to_display)
        self._create_and_show_charts_with_data(per_chart_data, trade_data=None)

    def render_charts_with_trades(self, indicators_history, trade_history, *indicators_to_display):
        per_chart_data = self.__get_indicators_data_per_chart(indicators_history, indicators_to_display)
        per_chart_trade_data = None if trade_history is None \
            else self.__get_trade_data_per_chart(indicators_history, trade_history)

        self._create_and_show_charts_with_data(per_chart_data, per_chart_trade_data)

    def __get_indicators_data_per_chart(self, indicators_history: IndicatorHistory, indicators_to_display):
        per_chart_data = []
        timestamp, last_data_snapshot_object = indicators_history.last_snapshot_per_indicator_names_per_day
        for indicator_per_chart_collection in indicators_to_display:

            all_data_series_with_color_per_chart = []
            for series_indicator_name, color in indicator_per_chart_collection:
                data_per_series = last_data_snapshot_object.get_indicator_values_per_snapshot(series_indicator_name)

                # each data record will consists of: series (indicator) name, data per that indicator and its color
                all_data_series_with_color_per_chart.append((series_indicator_name, data_per_series, color))

            per_chart_data.append(all_data_series_with_color_per_chart)

        return per_chart_data

    def __get_trade_data_per_chart(self, indicators_history: IndicatorHistory, trade_history: TradeHistory):
        time_stamp, last_snapshot = indicators_history.last_snapshot_per_indicator_names_per_day
        price_bar_values = last_snapshot.get_indicator_values_per_snapshot('pricebar')

        index = 0
        result = []
        # find matching timestamps to make sure we can find index of transaction on the chart
        for time_stamp in [price_bar['timestamp'] for price_bar in price_bar_values]:
            for trade_record in trade_history.trade_records:
                if trade_record.trigger_price_bar.timestamp == time_stamp:
                    result.append((index, trade_record.transaction_type))
                    break
            index += 1

        return result

    @abc.abstractmethod
    def _create_and_show_charts_with_data(self, indicator_data_per_all_charts, trade_data):
        raise NotImplementedError("_create_and_show_charts_with_data")

    @property
    def chart_width(self):
        return self.__chart_width

    @property
    def chart_height(self):
        return self.__chart_height
