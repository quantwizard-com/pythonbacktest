from pythonbacktest.indicatorshistory import AbstractSnapshot
from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.ai.nodes.base.abstractnode import AbstractNode


class FunctionalNodeWithStore(AbstractNode):

    def __init__(self, node_name, function_to_call):
        super().__init__(node_name=node_name)
        self.__function_to_call = function_to_call
        self.__node_store = {}

    def _activation_method(self, indicators_snapshot: AbstractSnapshot,
                           trade_data_snapshot: TradeDataSnapshot) -> bool:
        return self.__function_to_call(indicators_snapshot, trade_data_snapshot, self.__node_store)

