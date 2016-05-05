from . import *
from bokeh.io import vplot
from bokeh.plotting import figure, show
from bokeh.models import BoxAnnotation
from bokeh.models.tools import BoxZoomTool, BoxSelectTool, CrosshairTool, \
    ResizeTool, ResetTool, HoverTool, PanTool, WheelZoomTool


class BokehChartRenderer(AbstractChartRendered):

    CHART_TOOLBAR_LOCATION = 'left'

    def __init__(self, width=900, height=500):
        AbstractChartRendered.__init__(self, width, height)

    def render_indicators(self, indicators, markers, *name_collections):

        all_charts = []
        first_chart = None

        for name_collection in name_collections:
            # for each collection we will have collection of indicator names and color

            new_chart = self.__create_chart(first_chart.x_range if first_chart is not None else None)
            all_charts.append(new_chart)

            if first_chart is None:
                first_chart = new_chart

            for indicator_name, color in name_collection:
                indicator_data = indicators.get_all_values_for_indicator(indicator_name)
                self.__add_data_to_chart(new_chart, indicator_data, {'color': color, 'line_width': 2})

            self.__add_markers_to_chart(new_chart, indicators, markers)

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

    def __create_chart(self, x_range=None):
        newchart = figure(title='', width=self.chart_width, height=self.chart_height,
                          tools=self.__create_chart_tools(), toolbar_location=self.CHART_TOOLBAR_LOCATION)
        newchart.grid.grid_line_dash = [4, 2]

        if x_range is not None:
            newchart.x_range = x_range

        return newchart

    def __add_data_to_chart(self, target_chart, data, chartparams):

        x_data, y_data = self.__pack_data_with_index(data)

        # unpack data for x and y
        target_chart.line(x_data, y_data, **chartparams)

    def __add_markers_to_chart(self, target_chart, indicators, markers):

        if markers is not None:
            for single_marker in markers:
                indicator_data = indicators.get_all_values_for_indicator(single_marker)
                x_data, y_data = self.__pack_data_with_index(indicator_data)

                # render markers
                target_chart.circle(x_data, y_data, size=15, fill_color='white', line_color='green', line_width=3)

    def __pack_data_with_index(self, data):

        # add 0-based indexes to the data
        chart_data = zip([t for t in range(0, len(data))], data)

        # filter out all tuples, where there's at least one None
        chart_data = [(x, y) for (x, y) in chart_data if y is not None]

        return [x for (x, y) in chart_data], [y for (x, y) in chart_data]


