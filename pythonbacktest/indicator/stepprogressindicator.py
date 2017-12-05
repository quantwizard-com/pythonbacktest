# simple moving average calculation
from .base import AbstractIndicator


class StepProgressIndicator(AbstractIndicator):

    def __init__(self, indicator_name, step_jump, source_indicators=None):
        AbstractIndicator.__init__(self,
                                   indicator_name=indicator_name,
                                   source_indicators=source_indicators)

        self.__step_jump = step_jump
        self.reset()

    def reset(self):
        AbstractIndicator.reset(self)
        self.__last_step_level = None

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()

        if new_value is None:
            self.add_new_result(None)
            return

        if self.__last_step_level is None or abs(self.__last_step_level - new_value) >= self.__step_jump:
            self.__last_step_level = new_value

        self.add_new_result(self.__last_step_level)
