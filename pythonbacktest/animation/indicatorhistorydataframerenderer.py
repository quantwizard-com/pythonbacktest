import numpy

class IndicatorHistoryDataFrameRenderer(object):

    @staticmethod
    def render_indicator_data(plots_per_axis, snapshot_data, ymin, ymax, progress_plot, progress_bar_location):
        # draw individual indicators
        for indicator_name, plot in plots_per_axis.items():
            snapshot_data_per_indicator = snapshot_data[indicator_name]

            x_data, y_data = IndicatorHistoryDataFrameRenderer.__pack_data_with_index(snapshot_data_per_indicator)

            plot.set_data(x_data, y_data)

            # set progress bar
            progress_bar_x = progress_bar_location
            progress_plot.set_data(progress_bar_x, [ymin, ymax])

            yield plot

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
                value = record[count] if is_tuple else record

                if value is not None:
                    result_x.append(current_x)
                    result_y.append(value)

                current_x += 1

            if count < tuple_len - 1:
                result_x.append(numpy.nan)
                result_y.append(numpy.nan)


        return result_x, numpy.array(result_y)



