from pythonbacktest.visualization import AbstractDataVisualization
from . import *
from matplotlib import pyplot as plt
import numpy


class IndicatorsHistoryAnimation(IPythonChartAnimation, AbstractDataVisualization):

    TRADE_MARKER_COLORS = {"BUY": "green", "SELL": "red", "SHORT": "purple"}
    CHART_TEXT_FORMAT = "X = %d"
    MAX_X_POINTS_PER_FRAME = 1000

    def __init__(self):

        AbstractDataVisualization.__init__(self)
        IPythonChartAnimation.__init__(self)

        # all chart plots; dictionary, where:
        # - key: name of the indicator
        # - value: chart plot

        self.__all_axes_plots = []
        self.__all_axes = []
        self.__indicator_snapshot = []
        self.__data_range_start = None
        self.__data_range_end = None
        self.__points_per_frame = None

    def render_animation(self, date, canvas_size, interval=20, fps=10, data_range=(0, None)):

        # calculate number of frames
        self.__indicator_snapshot = self.indicators_history.get_indicator_history_for_day(date)

        range_start, range_end = data_range

        self.__data_range_start = range_start

        number_of_snapshots = len(self.__indicator_snapshot)
        self.__data_range_end = range_end \
            if (range_end is not None and range_end < number_of_snapshots) \
            else number_of_snapshots - 1

        number_of_frames = self.__data_range_end - self.__data_range_start + 1

        if number_of_frames < 0:
            raise ValueError("Number of frames cannot be negative. Range setting: " + data_range)

        # maximum number of horizontal points (x-axis) visible on the screen in the same time
        # e.g.: 1000 means x can have values between (0, 999), (1, 1000), etc.
        self.__points_per_frame = self.MAX_X_POINTS_PER_FRAME \
            if self.MAX_X_POINTS_PER_FRAME < number_of_frames \
            else number_of_frames

        target_canvas = plt.figure(figsize=canvas_size)

        # on the create canvas - create all charts and chart text
        self.__create_all_chart_rows()

        # time to start the animation
        self._start_animation(animation_callback=self._animate_callback,
                              init_animation_callback=self._init_animation,
                              target_canvas=target_canvas,
                              frames=number_of_frames,
                              interval=interval,
                              fps=fps)

    def _init_animation(self):
        for axis_data in self.__all_axes_plots:
            for indicator_name, plot in axis_data['plots'].items():
                plot.set_data([], [])
                yield plot

    def _animate_callback(self, animation_frame_index):
        single_snapshot = list(self.__indicator_snapshot)[animation_frame_index + self.__data_range_start]

        snapshot_data = single_snapshot[1].snapshot_data

        # enumerate all axes and assign data to each one of those
        for axis_data in self.__all_axes_plots:
            plots_per_axis = axis_data['plots']
            markers_per_axis = axis_data['markers']
            progress_plot = axis_data['progress']
            zero_line_plot = axis_data['zeroline']
            ymin = axis_data['ymin']
            ymax = axis_data['ymax']
            xmin = axis_data['xmin']
            xmax = axis_data['xmax']

            close_indicator_in_data = False

            max_x_data = None

            # draw individual indicators
            for indicator_name, plot in plots_per_axis.items():
                snapshot_data_per_indicator = snapshot_data[indicator_name]

                x_data, y_data = self.__pack_data_with_index(snapshot_data_per_indicator)
                max_x_data = x_data[-1]

                plot.set_data(x_data, y_data)

                # set progress bar
                progress_bar_x = [x_data[-1]] * 2
                progress_plot.set_data(progress_bar_x, [ymin, ymax])

                if indicator_name == 'close':
                    close_indicator_in_data = True

                yield plot

            # draw transactions
            for transaction_name, plot in markers_per_axis.items():
                y_average = None
                if not close_indicator_in_data:
                    # we don't have close data, so we have to replace marker y with average between ymin and ymax
                    y_average = ymin + ((ymax - ymin) / 2)

                x_data, y_data = self.__pack_transactions_data_into_numpy_arrays(
                    transaction_name, max_x_data, replacement_data=y_average)

                plot.set_data(x_data, y_data)
                yield plot

            # draw zero-line
            zero_line_plot.set_data([xmin, xmax], [0, 0])

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

    def __create_all_chart_rows(self):
        all_charts_count = len(self.indicators_name_collections)
        current_axis_id = 1

        for indicators_with_colors in self.indicators_name_collections:
            # unpack collection of collections of charts
            x_min, x_max, y_min, y_max = self.__find_chart_boundaries(self.__indicator_snapshot, indicators_with_colors)

            ax = plt.subplot(all_charts_count, 1, current_axis_id)
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.grid(True)
            self.__all_axes.append(ax)

            self.__all_axes_plots.append({'axis': ax,
                                    'plots': self.__create_all_plots_per_axis(ax, indicators_with_colors),
                                    'markers': self.__create_all_markers_per_axis(ax),
                                    'progress': self.__create_progress_bar_per_axis(ax),
                                    'zeroline': self.__create_zero_line(ax),
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

    def __create_all_markers_per_axis(self, ax):

        all_markers_plots = {}

        for marker_name in self.recorded_transaction_names:
            single_marker_plot, = ax.plot(
                [], [],
                marker='D', markersize=5,
                color=self.TRADE_MARKER_COLORS[marker_name], lw=0)
            all_markers_plots[marker_name] = single_marker_plot

        return all_markers_plots

    def __create_progress_bar_per_axis(self, ax):
        single_progress_bar_plot, = ax.plot([], [], color='black', lw=1, ls=':')
        return single_progress_bar_plot

    def __create_zero_line(self, ax):
        zero_line, = ax.plot([], [], color='red', lw=2)
        return zero_line

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
        for timestamp, indicator_snapshot in list(indicator_snapshots)[self.__data_range_start:self.__data_range_end]:

            all_y_min_values_per_snapshot = []
            all_y_max_values_per_snapshot = []

            for indicator_name, snapshot_all_values in indicator_snapshot.snapshot_data.items():

                if indicator_name in indicators or not indicators:
                    values_filtered_none = [t for t in snapshot_all_values[self.__data_range_start:self.__data_range_end] if t is not None]

                    flat_values = []
                    # some values may be tuples, so extract individual values and calculate minimum
                    for value in values_filtered_none:
                        if type(value) == tuple:
                            flat_values.extend([t for t in value if t is not None])
                        else:
                            flat_values.append(value)

                    if len(flat_values) > 0:
                        all_y_min_values.append(min(flat_values))
                        all_y_max_values.append(max(flat_values))

            if len(all_y_min_values) > 0:
                all_y_min_values_per_snapshot.append(min(all_y_min_values))

            if len(all_y_max_values) > 0:
                all_y_max_values_per_snapshot.append(max(all_y_max_values))

        y_min = min(all_y_min_values_per_snapshot)
        y_max = max(all_y_max_values_per_snapshot)

        return x_min, x_max, y_min, y_max

    def __pack_transactions_data_into_numpy_arrays(self, transaction_name, max_x_data, replacement_data=None):
        result_x = []
        result_y = []

        if transaction_name in self.trade_transactions:
            for transaction_data in self.trade_transactions[transaction_name]:

                transaction_index, transaction_value = transaction_data

                if transaction_index <= max_x_data:
                    if replacement_data is not None:
                        transaction_value = replacement_data

                    # add index twice, since for each index we need to add value AND NaN value
                    result_x.append(transaction_index)
                    result_x.append(transaction_index)

                    result_y.append(transaction_value)
                    result_y.append(numpy.nan)

        return result_x, numpy.array(result_y)

    @staticmethod
    def __pack_data_with_index(data, y_replacement=None):

        result_x = []
        result_y = []

        is_tuple = False
        tuple_len = 1

        # 1 scan data for any tuples and find length of that tuple
        for record in data:
            if type(record) == tuple:
                tuple_len = len(record)
                is_tuple = True
                break

        for count in range(0, tuple_len):

            current_x = 0

            for record in data:
                if is_tuple:
                    value = numpy.nan if (record is None or record[count] is None)\
                        else y_replacement if y_replacement is not None\
                        else record[count]
                else:
                    value = numpy.nan if (record is None or record is None) \
                        else y_replacement if y_replacement is not None \
                        else record

                result_x.append(current_x)
                result_y.append(value)

                current_x += 1

            if count < tuple_len - 1:
                result_x.append(0)
                result_y.append(numpy.nan)

        return result_x, numpy.array(result_y)