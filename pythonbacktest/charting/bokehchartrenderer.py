from . import *
import numpy
from bokeh.io import vplot
from bokeh.plotting import figure, show
from bokeh.models.tools import BoxZoomTool, BoxSelectTool, CrosshairTool, \
    ResizeTool, ResetTool, HoverTool, PanTool, WheelZoomTool


class BokehChartRenderer(AbstractChartRendered):

    CHART_TOOLBAR_LOCATION = 'left'
    CHART_MARKER_SIZE = 10

    TRADE_MARKER_COLORS = {"trade_buy": "green", "trade_sell": "red", "trade_short": "purple"}

    def __init__(self, width=900, height=500):
        AbstractChartRendered.__init__(self, width, height)

    def render_indicators(self, indicators_snapshot, markers, *name_collections):

        all_charts = []
        first_chart = None

        for name_collection in name_collections:
            # for each collection we will have collection of indicator names and color
            chart_title = self.__generate_chart_title(name_collection)
            new_chart = self.__create_chart(first_chart.x_range if first_chart is not None else None,
                                            title=chart_title)
            all_charts.append(new_chart)

            if first_chart is None:
                first_chart = new_chart

            average_value = None
            set_markers_at_average = True
            for indicator_name, color in name_collection:
                indicator_data = indicators_snapshot.snapshot_data[indicator_name]
                self.__add_data_to_chart(new_chart, indicator_data, {'color': color, 'line_width': 2})

                average_data = self.__average_indicator_data(indicator_data)
                if average_value is None:
                    average_value = average_data
                else:
                    average_value = (average_data + average_value) / 2

                if indicator_name == 'close':
                    set_markers_at_average = False

            #self.__add_markers_to_chart(new_chart, indicators_snapshot, markers, average_value, set_markers_at_average)

        if len(all_charts) == 1:
            show(first_chart)
        else:
            show(vplot(*all_charts))

    def render_trades(self, trade_log):
        pass

    def __create_chart_tools(self):
        hover = HoverTool(
            tooltips=[
                ("x", "$x"),
                ("y", "$y")]
        )
        return [BoxZoomTool(), BoxSelectTool(), PanTool(), WheelZoomTool(), CrosshairTool(), ResizeTool(), ResetTool(), hover]

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

            # check of we have tupple of values
            if isinstance(y_data, tuple):
                y_data = list(y_data)
            else:
                y_data = [y_data]

            for y_record in y_data:
                if y_record is None:
                    raise ValueError("y_record is None for some reason...")

                target_chart.line(x_data, y_record, **chartparams)

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
        result = [[] for x in xrange(number_of_series_in_data)]
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

    def __add_markers_to_chart(self, target_chart, indicators_snapshot, markers, average_value, set_markers_at_average):

        if markers is not None:
            for single_marker in markers:
                indicator_data = indicators_snapshot.snapshot_data[single_marker]

                y_replacement = average_value if set_markers_at_average else None

                x_data, y_data = self.__pack_data_with_index(indicator_data, y_replacement=y_replacement)

                # render markers
                target_chart.circle(x_data, y_data, size=self.CHART_MARKER_SIZE,
                                    fill_color='white', line_color=self.TRADE_MARKER_COLORS[single_marker],
                                    line_width=3)

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
            result_x.append(current_x)

            current_y = record if y_replacement is None else y_replacement if record is not None else None
            result_y.append(current_y if current_y is not None else numpy.nan)

            current_x += 1

        return result_x, numpy.array(result_y)

    def __average_indicator_data(self, indicator_data):

        try:
            return numpy.mean([t for t in indicator_data if t is not None])
        except:
            print len(indicator_data)
            print indicator_data
            return 0

    def __generate_chart_title(self, name_color_collection):
        indicator_names = [t[0] for t in name_color_collection]
        return ', '.join(indicator_names)




