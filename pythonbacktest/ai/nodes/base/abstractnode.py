from abc import abstractmethod, ABC

from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.indicatorshistory import AbstractSnapshot


class AbstractNode(ABC):

    def __init__(self, node_name):
        self.__node_name = node_name
        self.__indicators_history_source = None
        self.__node_result: bool = None

    @property
    def node_name(self):
        return self.__node_name

    @property
    def current_node_result(self) -> bool:
        return self.__node_result

    def set_node_result(self, result):
        self.__node_result = result

    def activate_node(self, indicators_snapshot: AbstractSnapshot, trade_data_snapshot: TradeDataSnapshot) -> bool:
        """
        Activate node and return the node result
        :param indicators_snapshot: Indicators snapshot
        :param trade_data_snapshot
        :return: Boolean result on the node - depending on the node evaluation result
        """
        self.set_node_result(self._activation_method(indicators_snapshot, trade_data_snapshot))
        return self.current_node_result

    @abstractmethod
    def _activation_method(self, indicators_snapshot: AbstractSnapshot, trade_data_snapshot: TradeDataSnapshot) -> bool:
        raise NotImplementedError()
