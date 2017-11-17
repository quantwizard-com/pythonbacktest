from typing import Dict

from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.indicatorshistory import AbstractSnapshot
from pythonbacktest.ai.nodemanager.nodesmap import NodesMap


class NodesProcessor(object):

    def __init__(self, source_nodes_map: NodesMap):
        self.__source_nodes_map = source_nodes_map

    def new_data_snapshots(self, indicators_snapshot: AbstractSnapshot,
                           trade_data_snapshot: TradeDataSnapshot) -> Dict:
        """
        :param indicators_snapshot:
        :param trade_data_snapshot:
        :return: Dictionary: node name with node result
        """
        return self.__source_nodes_map.apply_data_snapshots(
            indicators_snapshot=indicators_snapshot, trade_data_snapshot=trade_data_snapshot)


