from . import *
from matplotlib import pyplot as plt
import sys

class IndicatorsHistoryAnimation(IPythonAnimation):

    def __init__(self, frames=100, interval=20):
        IPythonAnimation.__init__(self, frames, interval)

    def __init_animation(self):
        raise NotImplementedError()

    def __animate_callback(self, animation_parameter):
        pass

    def __animate_indicators(self, indicator_history, indicator_date):
        pass

    # find min and max values for x and y axis
    # - input: sorted (by timestamp) list of tuples: (timestamp, indicator snapshot)
    # - output: tuple - (x_min, x_max, y_min, y_max)
    def __find_chart_boundaries(self, indicator_snapshots):
        # we need only check the last record - as it contains all values for all indicators
        all_y_max_values = []
        all_y_min_values = []

        timestamp, indicator_snapshot = indicator_snapshots[-1]

        x_min = 0
        x_max = -1

        for snapshot_name, snapshot_all_values in indicator_snapshot.snapshot_data:
            if x_max == -1:
                x_max = len(snapshot_all_values) - 1

            all_y_max_values.append(max(snapshot_all_values))
            all_y_min_values.append(min(snapshot_all_values))

        y_min = min(all_y_min_values)
        y_max = min(all_y_max_values)

        return x_min, x_max, y_min, y_max
