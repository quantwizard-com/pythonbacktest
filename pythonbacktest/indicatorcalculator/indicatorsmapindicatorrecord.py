class IndicatorsMapIndicatorRecord(object):

    def __init__(self, indicator_name, indicator_sources, indicator_implementation):
        """
        Set the indicator map
        :param indicator_name: Name of the indicator
        :param indicator_sources: List of names of the source indicators; could be passed in following form:
        - single indicator source
        - collection of the indicator sources
        Has to be set to non-empty value.
        :param indicator_implementation:
        """

        self.__indicator_name = indicator_name
        self.__indicator_sources = indicator_sources
        self.__indicator_implementation = indicator_implementation
