from pythonbacktest.ai.nodes import AbstractNode


class DataCrossNode(AbstractNode):
    """
    Node detecting whenever there was a cross between 2 data streams, e.g.:
    Detect cross between SMAs
    """

    def __init__(self):
        self.__serie1 = []
        self.__serie2 = []
        self.__all_result_values = []
        self.__current_value = None
        self.__previous_serie1_value = None
        self.__previous_serie2_value = None

    @property
    def current_value(self):
        return self.__current_value

    @property
    def all_collected_values(self):
        return self.__serie1, self.__serie2, self.__all_result_values

    def reset_node(self):
        pass

    def inject_data(self, **kwargs):
        pass
