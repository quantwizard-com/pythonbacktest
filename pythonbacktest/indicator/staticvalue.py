from .abstractindicator import AbstractIndicator

class StaticValue(AbstractIndicator):

    def __init__(self):
        AbstractIndicator.__init__(self)
        self.reset()

    def reset(self):
        self.__current_value = None
        self.__all_values = []

    @property
    def result(self):
        return self.__current_value

    @property
    def all_result(self):
        return self.__all_values

    def on_new_upstream_value(self, new_value):

        if type(new_value) is list:
            raise ValueError("StaticValue doesn't handle lists")

        self.__current_value = new_value
        self.all_result.append(new_value)
