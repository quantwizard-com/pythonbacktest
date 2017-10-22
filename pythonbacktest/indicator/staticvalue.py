from .abstractindicator import AbstractIndicator


class StaticValue(AbstractIndicator):

    def __init__(self, indicator_name, source_indicators=None):
        if source_indicators is not None and len(source_indicators) != 1:
            raise ValueError("Expecting 1 source indicator only")

        AbstractIndicator.__init__(self,
                                   indicator_name=indicator_name,
                                   source_indicators=source_indicators)
        self.reset()

    def reset(self):
        AbstractIndicator.reset(self)

    def _process_new_upstream_record(self):
        new_value = self.get_latest_data_from_source_indicators()

        self.all_results.append(new_value)
