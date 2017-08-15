from . import *
import numpy
import sys
from bokeh.models.layouts import Column
from bokeh.plotting import figure, show
from bokeh.models.tools import BoxZoomTool, BoxSelectTool, CrosshairTool, \
    ResizeTool, ResetTool, HoverTool, PanTool, WheelZoomTool, SaveTool


class BokehChartRenderer(AbstractChartRenderer):

    CHART_TOOLBAR_LOCATION = 'left'
    CHART_MARKER_SIZE = 10

    TRADE_MARKER_COLORS = {"BUY": "green", "SELL": "red", "SHORT": "purple"}

    def __init__(self, width=900, height=500):
        AbstractChartRenderer.__init__(self, width, height)

    def render_charts(self, date_to_display, sigma_data=None):
        all_charts = []
        first_chart = None

        for name_collection in self.indicators_name_collections:
            # for each collection we will have collection of indicator names and color
            chart_title = self.__generate_chart_title(name_collection)
            new_chart = self.__create_chart(first_chart.x_range if first_chart is not None else None,
                                            title=chart_title)
            all_charts.append(new_chart)

            if first_chart is None:
                first_chart = new_chart

            average_value = None
            set_markers_at_average = True

            # get last data snapshot for the given day
            indicators_snapshot = self.indicators_history.get_last_indicator_snapshot_per_day(date_to_display)

            min_per_chart = []
            max_per_chart = []

            for indicator_name, color in name_collection:
                # check if we want to add sigma data for this indicator
                if sigma_data is not None and indicator_name in sigma_data:
                    self.__add_sigma_data(new_chart, sigma_data[indicator_name], len(indicator_data))

            for indicator_name, color in name_collection:
                indicator_data = indicators_snapshot.snapshot_data[indicator_name]
                self.__add_data_to_chart(new_chart, indicator_data, {'color': color, 'line_width': 2, 'legend': indicator_name })

                average_data, min_data, max_data = self.__average_indicator_data(indicator_data)
                min_per_chart.append(min_data)
                max_per_chart.append(max_data)

                if average_value is None:
                    average_value = average_data
                else:
                    average_value = (average_data + average_value) / 2

                if indicator_name == 'close':
                    set_markers_at_average = False

            self.__add_trade_log_to_chart(new_chart, average_value, set_markers_at_average)

            if min(min_per_chart) < 0 < max(max_per_chart):
                self.__add_zero_line_to_chart(new_chart, len(indicator_data))

        if len(all_charts) == 1:
            show(first_chart)
        else:
            show(Column(*all_charts))

    def __create_chart_tools(self):
        hover = HoverTool(
            tooltips=[
                ("x", "$x"),
                ("y", "$y")]
        )
        return [SaveTool(), BoxZoomTool(), BoxSelectTool(), PanTool(), WheelZoomTool(), CrosshairTool(), ResizeTool(), ResetTool(), hover]

    def __create_chart(self, x_range=None, title=''):
        newchart = figure(title=title, width=self.chart_width, height=self.chart_height,
                          tools=self.__create_chart_tools(), toolbar_location=self.CHART_TOOLBAR_LOCATION)
        newchart.grid.grid_line_dash = [4, 2]

        if x_range is not None:
            newchart.x_range = x_range

        return newchart

    def __add_data_to_chart(self, target_chart, data_collection, chartparams):
        for data in self.__split_data_into_lists(data_collection):
            x_data, y_data = self.__pack_data_with_index(data)

            target_chart.line(x_data, y_data, **chartparams)

    # chart renderer may consume data consisting of multiple series, but which should be redered on single chart
    # example: minmax tracker, which tracks minimum and maximum values, thus consists of 2 series
    # data is served as collection of tuples - values per each serie at the given moment in time
    # it has to be split into collection of series instead
    def __split_data_into_lists(self, data):
        number_of_series_in_data = None

        # find out what's the length of the tuples in data
        for record in data:
            if record is not None:
                number_of_series_in_data = 1
                if isinstance(record, tuple):
                    number_of_series_in_data = len(record)
                break

        if number_of_series_in_data is None:
            # data is just collection of Nones - so the size is 1
            number_of_series_in_data = 1

        if number_of_series_in_data == 1:
            return [data]

        # actual split
        result = [[] for x in range(number_of_series_in_data)]
        for record in data:
            if record is None:
                for result_list in result:
                    result_list.append(None)
            else:
                index = 0
                for result_list in result:
                    result_list.append(record[index])
                    index += 1

        return result

    def __add_trade_log_to_chart(self, target_chart, average_value, set_markers_at_average):

        if self.trade_transactions is not None:
            for transaction_name, transaction_data in self.trade_transactions.items():

                for price_bar_index, transaction_price_per_share in transaction_data:
                    y_data = average_value if set_markers_at_average else transaction_price_per_share

                    # render markers
                    target_chart.circle(price_bar_index, y_data, size=self.CHART_MARKER_SIZE,
                                        fill_color='white', line_color=self.TRADE_MARKER_COLORS[transaction_name],
                                        line_width=3)

    def __add_zero_line_to_chart(self, target_chart, data_len):
        target_chart.line([0, data_len], [0, 0], line_color='red', line_width=1)

    def __add_sigma_data(self, target_chart, sigma_data, data_len):
        mean, sigma_records = sigma_data
        target_chart.line([0, data_len], [mean, mean], line_color='green', line_width=1)

        for sigma_level, sigmas in sigma_records.items():
            (std_minus, std_plus), percentage = sigmas
            target_chart.hbar(y=mean, height=std_plus - std_minus, right=data_len, fill_alpha=0.1, color='#888888')
        return

    def __pack_data_with_index(self, data, y_replacement=None):

        if data is None:
            raise ValueError("data is None")

        result_x = []
        result_y = []

        current_x = 0

        # 1. take all records in data
        # 2. assign index (0-based to each record)
        # 3. filter-out records AND corresponding index for records = None
        for record in data:
            if record is not None:
                result_x.append(current_x)

                current_y = record if y_replacement is None else y_replacement
                result_y.append(current_y)

            current_x += 1

        return result_x, numpy.array(result_y)

    def __average_indicator_data(self, indicator_data):

        y_not_none = [t for t in [self.__average_single_y(y) for y in indicator_data] if t is not None]

        return numpy.mean(y_not_none), min(y_not_none), max(y_not_none)

    def __average_single_y(self, y):
        """
        In some cases y may consists of tumple, in which case that tuple has to be averaged
        :return: Averaged y
        """
        if type(y) is tuple:
            y_not_none = [t for t in list(y) if t is not None]
            if y_not_none:
                return numpy.mean(y_not_none)
            else:
                return None
        else:
            return y

    def __generate_chart_title(self, name_color_collection):
        indicator_names = [t[0] for t in name_color_collection]
        return ', '.join(indicator_names)






