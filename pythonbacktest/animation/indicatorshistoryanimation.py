from . import *
from matplotlib import pyplot as plt


class IndicatorsHistoryAnimation(IPythonAnimation):

    def __init__(self, indicators_history, date, interval=20):

        # all chart plots; dictionary, where:
        # - key: name of the indicator
        # - value: chart plot
        self.__all_chart_plots = {}
        self.__indicator_snapshot = indicators_history.get_indicator_history_for_day(date)
        self.__create_all_charts(indicators_history)
        self.__number_of_frames = len(self.__indicator_snapshot)

        IPythonAnimation.__init__(self, self.__number_of_frames, interval)

    def _init_animation(self):
        # init all chart plots
        for indicator_name, single_chart_plot in self.__all_chart_plots.iteritems():
            single_chart_plot.set_data([], [])

    def _animate_callback(self, animation_frame_index):
        single_snapshot = self.__indicator_snapshot[animation_frame_index]

        snapshot_data = single_snapshot[animation_frame_index]

        # for now: all x-data will come as a data index
        x_data = [t for t in range(0, self.__number_of_frames)]

        # fill individual charts with data from the snapshot
        for indicator_name, single_chart_plot in self.__all_chart_plots:
            snapshot_data_per_indicator = snapshot_data[indicator_name]

            single_chart_plot.set_data(x_data, snapshot_data_per_indicator)

    def __create_all_charts(self, indicators_history):
        indicator_names = indicators_history.all_indicator_names

        x_min, x_max, y_min, y_max = self.__find_chart_boundaries(self.__indicator_snapshot)

        ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))

        for single_indicator_name in indicator_names:
            single_chart_plot, = ax.plot([], [], lw=2)
            self.__all_chart_plots[single_indicator_name] = single_chart_plot

    # find min and max values for x and y axis
    # - input: sorted (by timestamp) list of tuples: (timestamp, indicator snapshot)
    # - output: tuple - (x_min, x_max, y_min, y_max)
    def __find_chart_boundaries(self, indicator_snapshots):
        # we need only check the last record - as it contains all values for all indicators
        all_y_max_values = []
        all_y_min_values = []

        timestamp, indicator_snapshot = indicator_snapshots[-1]

        # x goes (for now) between 0 and maximum number of elements minus 1
        # the assumption: all data for all indicators will have the same length
        x_min = 0
        x_max = -1

        for snapshot_name, snapshot_all_values in indicator_snapshot.snapshot_data.iteritems():
            if x_max == -1:
                x_max = len(snapshot_all_values) - 1

            values_filtered_none = [t for t in snapshot_all_values if t is not None]
            if len(values_filtered_none) > 0:
                all_y_max_values.append(max(values_filtered_none))
                all_y_min_values.append(min(values_filtered_none))

            y_min = min(all_y_min_values)
        y_max = max(all_y_max_values)

        return x_min, x_max, y_min, y_max
