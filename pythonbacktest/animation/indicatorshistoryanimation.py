from . import *
from matplotlib import pyplot as plt


class IndicatorsHistoryAnimation(IPythonAnimation):

    def __init__(self, indicators_history, date, interval=20, indicators=[]):

        # all chart plots; dictionary, where:
        # - key: name of the indicator
        # - value: chart plot

        self.__all_chart_plots = {}
        self.__indicator_snapshot = indicators_history.get_indicator_history_for_day(date)
        number_of_frames = len(self.__indicator_snapshot)

        # we need to create the target canvas (figure)
        IPythonAnimation.__init__(self, number_of_frames, interval)

        # on the create canvas - create all charts
        self.__create_all_charts(indicators)

    def _init_animation(self):
        # init all chart plots
        for indicator_name, single_chart_plot in self.__all_chart_plots.iteritems():
            single_chart_plot.set_data([], [])
            yield single_chart_plot

    def _animate_callback(self, animation_frame_index):
        single_snapshot = self.__indicator_snapshot[animation_frame_index]

        snapshot_data = single_snapshot[1].snapshot_data

        # for now: all x-data will come as a data index
        x_data = None

        # fill individual charts with data from the snapshot
        for indicator_name, single_chart_plot in self.__all_chart_plots.iteritems():
            snapshot_data_per_indicator = snapshot_data[indicator_name]

            if x_data is None:
                x_data = [t for t in range(0, len(snapshot_data_per_indicator))]

            single_chart_plot.set_data(x_data, snapshot_data_per_indicator)
            yield single_chart_plot

    #
    # HELP SET-UP METHODS
    #

    def __create_all_charts(self, indicators_with_colors):
        x_min, x_max, y_min, y_max = self.__find_chart_boundaries(self.__indicator_snapshot, indicators_with_colors)

        ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))

        for indicator_name, indicator_color in indicators_with_colors:
            single_chart_plot, = ax.plot([], [],color=indicator_color, lw=2)
            self.__all_chart_plots[indicator_name] = single_chart_plot

    # find min and max values for x and y axis
    # - input: sorted (by timestamp) list of tuples: (timestamp, indicator snapshot)
    # - output: tuple - (x_min, x_max, y_min, y_max)
    def __find_chart_boundaries(self, indicator_snapshots, indicators_with_colors):
        # we need only check the last record - as it contains all values for all indicators
        all_y_max_values = []
        all_y_min_values = []

        timestamp, indicator_snapshot = indicator_snapshots[-1]

        # x goes (for now) between 0 and maximum number of elements minus 1
        # the assumption: all data for all indicators will have the same length
        x_min = 0
        x_max = -1

        indicators = [t[0] for t in indicators_with_colors]

        for indicator_name, snapshot_all_values in indicator_snapshot.snapshot_data.iteritems():
            if x_max == -1:
                x_max = len(snapshot_all_values) - 1

            if indicator_name in indicators or not indicators:
                values_filtered_none = [t for t in snapshot_all_values if t is not None]
                if len(values_filtered_none) > 0:
                    all_y_max_values.append(max(values_filtered_none))
                    all_y_min_values.append(min(values_filtered_none))

        y_min = min(all_y_min_values)
        y_max = max(all_y_max_values)

        return x_min, x_max, y_min, y_max
