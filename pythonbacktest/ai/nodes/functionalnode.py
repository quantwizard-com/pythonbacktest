from pythonbacktest.ai.utils.indicatorshistorysource import IndicatorsHistorySource
from pythonbacktest.ai.nodes.base.abstractnode import AbstractNode


class FunctionalNode(AbstractNode):

    def __init__(self, node_name, function_to_call):
        super().__init__(node_name=node_name)
        self.__function_to_call = function_to_call

    def _activation_method(self):
        result = self.__function_to_call(self.indicators_history_source)

