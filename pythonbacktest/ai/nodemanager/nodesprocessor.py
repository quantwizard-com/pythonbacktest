from typing import Dict

from indicatorshistory import AbstractSnapshot
from pythonbacktest.ai.nodemanager.nodesmap import NodesMap


class NodesProcessor(object):

    def __init__(self, source_nodes_map: NodesMap):
        self.__source_nodes_map = source_nodes_map

    def new_indicators_snapshot(self, indicators_snapshot: AbstractSnapshot) -> Dict:
        """
        :param indicators_snapshot:
        :return: Dictionary: node name with node result
        """
        return self.__source_nodes_map.apply_indicators_snapshot(indicators_snapshot=indicators_snapshot)


