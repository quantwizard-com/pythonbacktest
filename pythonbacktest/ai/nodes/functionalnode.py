from pythonbacktest.ai.utils.indicatorssource import IndicatorsSource
from pythonbacktest.ai.nodes.base.abstractnode import AbstractNode


class FunctionalNode(AbstractNode):

    def __init__(self, indicators_source: IndicatorsSource, function_to_call):
        super().__init__(indicators_source)
        self.__function_to_call = function_to_call

    def _activation_method(self):
        result = self.__function_to_call(self.indicators_source)

