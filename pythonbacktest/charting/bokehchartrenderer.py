import numpy
from bokeh.models import Title

from .abstractchartrenderer import AbstractChartRenderer
from bokeh.models.layouts import Column
from bokeh.plotting import figure, show
from bokeh.models.tools import BoxZoomTool, BoxSelectTool, CrosshairTool, \
    ResetTool, HoverTool, PanTool, WheelZoomTool, SaveTool


class BokehChartRenderer(AbstractChartRenderer):

    CHART_TOOLBAR_LOCATION = 'left'
    CHART_MARKER_SIZE = 10
    TRADE_TYPE_TO_COLOR = {'buy': 'green', 'sell': 'red', 'sshort': 'purple'}

    def __init__(self, width=900, height=500):
        AbstractChartRenderer.__init__(self, width, height)

    def _create_and_show_charts_with_data(self, indicator_data_per_all_charts, trade_data):
        all_charts = []
        for indicator_data_per_chart in indicator_data_per_all_charts:
            newchart = figure(width=self.chart_width, height=self.chart_height,
                              tools=BokehChartRenderer.__create_chart_tools(),
                              toolbar_location=self.CHART_TOOLBAR_LOCATION,
                              x_range=all_charts[0].x_range if all_charts else None
                              )
            newchart.grid.grid_line_dash = [4, 2]
            all_charts.append(newchart)

            self.__render_chart_title(newchart, indicator_data_per_chart)
            self.__render_chart_data(newchart, indicator_data_per_chart)

            if trade_data is not None:
                self.__render_trade_data(newchart, indicator_data_per_chart, trade_data)

        if len(all_charts) == 1:
            show(all_charts[0])
        else:
            show(Column(*all_charts))

    def __render_chart_data(self, target_chart, indicator_data_per_chart):
        for indicator_name, data_per_serie, color_per_serie in indicator_data_per_chart:
            x_data, y_data = self.__pack_data_with_index(data_per_serie)
            target_chart.line(x_data, y_data, **{'color': color_per_serie, 'line_width': 2, 'legend': indicator_name})

    def __render_chart_title(self, target_chart, indicator_data_per_chart):
        title_text = ",".join([data[0] for data in indicator_data_per_chart])
        target_chart.title = Title(text=title_text)

    def __render_trade_data(self, target_chart, indicator_data_per_chart, trade_data):
        # find max and min of all indicator data per chart
        max_value = max([max(data[1]) for data in indicator_data_per_chart])
        min_value = min([min(data[1]) for data in indicator_data_per_chart])

        for index, trade_type in trade_data:
            trade_type_lower = trade_type.lower()
            if trade_type_lower not in self.TRADE_TYPE_TO_COLOR:
                raise ValueError("Can't find trade type: " + trade_type)

            trade_color = self.TRADE_TYPE_TO_COLOR[trade_type_lower]
            target_chart.line([index, index], [min_value, max_value], **{'color': trade_color, 'line_width': 1})

    @staticmethod
    def __create_chart_tools():
        hover = HoverTool(
            tooltips=[
                ("x", "$x"),
                ("y", "$y")]
        )
        return [SaveTool(),
                BoxZoomTool(),
                BoxSelectTool(),
                PanTool(),
                WheelZoomTool(),
                CrosshairTool(),
                ResetTool(),
                hover]

    def __pack_data_with_index(self, data):

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

                current_y = record
                result_y.append(current_y)

            current_x += 1

        return result_x, numpy.array(result_y)





