from .base import AbstractIndicator

class DataDifference(AbstractIndicator):

    def __init__(self, indicator_name, source_indicators=None):
        AbstractIndicator.__init__(self,
                                   indicator_name=indicator_name,
                                   source_indicators=source_indicators)
        self.reset()

    def reset(self):
        AbstractIndicator.reset(self)

    def _process_new_upstream_record(self):
        value1, value2 = self.get_latest_data_from_source_indicators()

        result = value2 - value1 if None not in (value1, value2) else None

        self.all_results.append(result)
