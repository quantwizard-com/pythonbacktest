import abc


class AbstractIndicator(object):

    @abc.abstractmethod
    def reset(self):
        """
        Reset indicator to the initial value. It's called when IndicatorsCalculator
        starts calculation for single date
        :return: None
        """
        raise NotImplementedError()

    # get LATEST indicator value (as: latest value)
    @abc.abstractmethod
    def result(self):
        raise NotImplementedError()

    # return entire collection of results for the given indicator
    # e.g.: for SMA that would be all SMA values for the given input
    @abc.abstractmethod
    def all_result(self):
        raise NotImplementedError()

    # new value from one of the upstream indicator is ready and can be consumed
    @abc.abstractmethod
    def on_new_upstream_value(self, new_value):
        raise NotImplementedError()