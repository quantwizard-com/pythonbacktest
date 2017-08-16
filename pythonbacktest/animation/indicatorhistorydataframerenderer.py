import numpy

class IndicatorHistoryDataFrameRenderer(object):

    @staticmethod
    def render_indicator_data(plots_per_axis, snapshot_data, ymin, ymax, progress_plot):
        close_indicator_in_data = False

        max_x_data = None

        # draw individual indicators
        for indicator_name, plot in plots_per_axis.items():
            snapshot_data_per_indicator = snapshot_data[indicator_name]

            x_data, y_data = IndicatorHistoryDataFrameRenderer.__pack_data_with_index(snapshot_data_per_indicator)
            max_x_data = x_data[-1]

            plot.set_data(x_data, y_data)

            # set progress bar
            progress_bar_x = [x_data[-1]] * 2
            progress_plot.set_data(progress_bar_x, [ymin, ymax])

            if indicator_name == 'close':
                close_indicator_in_data = True

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
                if is_tuple:
                    value = numpy.nan if (record is None or record[count] is None) \
                        else y_replacement if y_replacement is not None \
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



