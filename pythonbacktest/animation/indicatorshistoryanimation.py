from . import *
from matplotlib import pyplot as plt
import numpy


class IndicatorsHistoryAnimation(IPythonAnimation):

    TRADE_MARKER_COLORS = {"trade_buy": "green", "trade_sell": "red", "trade_short": "purple"}
    CHART_TEXT_FORMAT = "X = %d"
    MAX_X_POINTS_PER_FRAME = 1000

    def __init__(self, indicators_history, date, indicators=[], interval=20, markers=[],
                 canvassize=None, datarange=(0, None)):

        # all chart plots; dictionary, where:
        # - key: name of the indicator
        # - value: chart plot

        self.__all_axes_plots = []
        self.__all_axes = []
        self.__indicator_snapshot = indicators_history.get_indicator_history_for_day(date)

        range_start, range_end = datarange

        self.__data_range_start = range_start

        number_of_snapshots = len(self.__indicator_snapshot)
        self.__data_range_end = range_end \
            if (range_end is not None and range_end < number_of_snapshots) \
            else number_of_snapshots - 1

        number_of_frames = self.__data_range_end - self.__data_range_start + 1

        if number_of_frames < 0:
            raise ValueError("Number of frames cannot be negative. Range setting: " + datarange)

        # we need to create the target canvas (figure)
        IPythonAnimation.__init__(self, number_of_frames, interval, canvassize=canvassize)

        # maximum number of horizontal points (x-axis) visible on the screen in the same time
        # e.g.: 1000 means x can have values between (0, 999), (1, 1000), etc.
        self.__points_per_frame = self.MAX_X_POINTS_PER_FRAME \
            if self.MAX_X_POINTS_PER_FRAME < number_of_frames \
            else number_of_frames

        # on the create canvas - create all charts and chart text
        self.__create_all_chart_rows(indicators, markers)

    def _init_animation(self):

        for axis_data in self.__all_axes_plots:
            for indicator_name, plot in axis_data['plots'].iteritems():
                plot.set_data([], [])
                yield plot

    def _animate_callback(self, animation_frame_index):
        single_snapshot = self.__indicator_snapshot[animation_frame_index + self.__data_range_start]

        snapshot_data = single_snapshot[1].snapshot_data

        # enumerate all axes and assign data to each one of those
        for axis_data in self.__all_axes_plots:
            plots_per_axis = axis_data['plots']
            markers_per_axis = axis_data['markers']
            ymin = axis_data['ymin']
            ymax = axis_data['ymax']

            close_indicator_in_data = False

            for indicator_name, plot in plots_per_axis.iteritems():
                snapshot_data_per_indicator = snapshot_data[indicator_name]

                x_data, y_data = self.__pack_data_with_index(snapshot_data_per_indicator)

                plot.set_data(x_data, y_data)

                if indicator_name == 'close':
                    close_indicator_in_data = True

                yield plot

            for marker_name, plot in markers_per_axis.iteritems():
                snapshot_data_per_marker = snapshot_data[marker_name]
                x_data, y_data = self.__pack_data_with_index(snapshot_data_per_marker)

                if not close_indicator_in_data:
                    # we don't have close data, so we have to replace marker y with average between ymin and ymax
                    y_avg = ymin + ((ymax - ymin) / 2)
                    y_data = [y_avg for y in y_data]

                plot.set_data(x_data, y_data)
                yield plot

        # calculate if chart should be moved on the x-axis to show data
        border_x_point = self.__points_per_frame - self.__points_per_frame * 0.2
        if animation_frame_index > border_x_point:
            translation = animation_frame_index - border_x_point
            x_min = self.__data_range_start + translation
            x_max = self.__data_range_start + self.__points_per_frame - 1 + translation

            for axis in self.__all_axes:
                axis.set_xlim(x_min, x_max)

    #
    # HELP SET-UP METHODS
    #

    def __create_all_chart_rows(self, indicators, marker_names):

        all_charts_count = len(indicators)
        current_axis_id = 1

        for indicators_with_colors in indicators:
            # unpack collection of collections of charts
            x_min, x_max, y_min, y_max = self.__find_chart_boundaries(self.__indicator_snapshot, indicators_with_colors)

            ax = plt.subplot(all_charts_count, 1, current_axis_id)
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.grid(True)
            self.__all_axes.append(ax)

            self.__all_axes_plots.append({'axis': ax,
                                    'plots': self.__create_all_plots_per_axis(ax, indicators_with_colors),
                                    'markers': self.__create_all_markers_per_axis(ax, marker_names),
                                    'xmin': x_min,
                                    'xmax': x_max,
                                    'ymin': y_min,
                                    'ymax': y_max})

            current_axis_id += 1

    def __create_all_plots_per_axis(self, ax, indicators_with_colors):

        all_axis_plots = {}

        for indicator_name, indicator_color in indicators_with_colors:
            single_chart_plot, = ax.plot([], [], color=indicator_color, lw=1)
            all_axis_plots[indicator_name] = single_chart_plot

        return all_axis_plots

    def __create_all_markers_per_axis(self, ax, marker_names):

        all_markers_plots = {}

        for marker_name in marker_names:
            single_marker_plot, = ax.plot(
                [], [],
                marker='D', markersize=5,
                color=self.TRADE_MARKER_COLORS[marker_name], lw=0)
            all_markers_plots[marker_name] = single_marker_plot

        return all_markers_plots

    # find min and max values for x and y axis
    # - input: sorted (by timestamp) list of tuples: (timestamp, indicator snapshot)
    # - output: tuple - (x_min, x_max, y_min, y_max)
    def __find_chart_boundaries(self, indicator_snapshots, indicators_with_colors):
        # we need only check the last record - as it contains all values for all indicators
        all_y_max_values = []
        all_y_min_values = []

        all_y_min_values_per_snapshot = []
        all_y_max_values_per_snapshot = []

        # x goes (for now) between 0 and maximum number of elements minus 1
        # the assumption: all data for all indicators will have the same length
        x_min = self.__data_range_start
        x_max = self.__data_range_start + self.__points_per_frame - 1

        indicators = [t[0] for t in indicators_with_colors]

        # get go through all indicators accross all timestamps to find the maximum y value
        # limit data based on the datarange
        for timestamp, indicator_snapshot in indicator_snapshots[self.__data_range_start:self.__data_range_end]:

            all_y_min_values_per_snapshot = []
            all_y_max_values_per_snapshot = []

            for indicator_name, snapshot_all_values in indicator_snapshot.snapshot_data.iteritems():

                if indicator_name in indicators or not indicators:
                    values_filtered_none = [t for t in snapshot_all_values[self.__data_range_start:self.__data_range_end] if t is not None]
                    if len(values_filtered_none) > 0:
                        all_y_min_values.append(min(values_filtered_none))
                        all_y_max_values.append(max(values_filtered_none))

            if len(all_y_min_values) > 0:
                all_y_min_values_per_snapshot.append(min(all_y_min_values))

            if len(all_y_max_values) > 0:
                all_y_max_values_per_snapshot.append(max(all_y_max_values))

        y_min = min(all_y_min_values_per_snapshot)
        y_max = max(all_y_max_values_per_snapshot)

        return x_min, x_max, y_min, y_max

    def __pack_data_with_index(self, data):

        result_x = []
        result_y = []

        current_x = 0

        # 1. take all records in data
        # 2. assign index (0-based to each record)
        # 3. filter-out records AND corresponding index for records = None
        for record in data:
            result_x.append(current_x)
            result_y.append(record if record is not None else numpy.nan)

            current_x += 1

        return result_x, numpy.array(result_y)
