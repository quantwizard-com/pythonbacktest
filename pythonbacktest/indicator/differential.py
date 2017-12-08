from .base import AbstractIndicator


class Differential(AbstractIndicator):

    def __init__(self, indicator_name, source_indicators=None):
        AbstractIndicator.__init__(self, indicator_name, source_indicators)

        self.reset()

    def reset(self):
        super().reset()
        self.__previous_value = None

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()
        previous_value = self.__previous_value

        diff = None

        if previous_value is not None and new_value is not None:
            diff = new_value - previous_value

        self.add_new_result(diff)
        self.__previous_value = new_value

