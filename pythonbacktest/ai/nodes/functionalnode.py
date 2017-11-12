from pythonbacktest.indicatorshistory import AbstractSnapshot
from pythonbacktest.ai.nodes.base.abstractnode import AbstractNode


class FunctionalNode(AbstractNode):

    def __init__(self, node_name, function_to_call):
        super().__init__(node_name=node_name)
        self.__function_to_call = function_to_call

    def _activation_method(self, indicators_snapshot: AbstractSnapshot):
        self.set_node_result(self.__function_to_call(indicators_snapshot))