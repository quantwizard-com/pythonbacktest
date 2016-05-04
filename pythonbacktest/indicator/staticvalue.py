from .abstractindicator import AbstractIndicator

class StaticValue(AbstractIndicator):

    def __init__(self):
        self.__current_value = None
        self.__all_values = None

    @property
    def result(self):
        return self.__current_value

    @property
    def all_result(self):
        return self.__all_values

    def on_new_upstream_value(self, new_value):
        self.__current_value = new_value
