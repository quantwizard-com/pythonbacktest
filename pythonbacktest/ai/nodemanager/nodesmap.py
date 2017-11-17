from typing import List, Dict

from pythonbacktest.ai.backoffice.tradehistory.tradedatasnapshot import TradeDataSnapshot
from pythonbacktest.indicatorshistory import AbstractSnapshot
from pythonbacktest.ai.nodes.base import AbstractNode


class NodesMap(object):

    def __init__(self, nodes_map_definition):
        self.__all_nodes: List[AbstractNode] = []
        self.__name_to_node_map = {}

        self.apply_node_map_definition(nodes_map_definition)

    def apply_node_map_definition(self, nodes_map_definition):
        self.__all_nodes = []
        self.__name_to_node_map = {}

        if not nodes_map_definition:
            return

        for record in nodes_map_definition:
            node_name, node_implementation = self.__unpack_node_map_definition(record)

            if node_name in self.__name_to_node_map:
                raise ValueError(f"Duplicate node name: {node_name}")

            self.__name_to_node_map[node_name] = node_implementation
            self.__all_nodes.append(node_implementation)

    def apply_data_snapshots(self, indicators_snapshot: AbstractSnapshot,
                             trade_data_snapshot: TradeDataSnapshot) -> Dict:
        """
        :param indicators_snapshot:
        :param trade_data_snapshot:
        :return: Dictionary: node name with node result
        """
        result = {}

        for single_node in self.__all_nodes:
            # indicators_source is already passed to each node, so doesn't have to pushed again
            result[single_node.node_name] = single_node.activate_node(indicators_snapshot, trade_data_snapshot)

        return result

    def __unpack_node_map_definition(self, record) -> tuple:
        node_implementation: AbstractNode = record['nodeimplementation']

        if not node_implementation:
            raise ValueError('Node implementation is not defined')

        return node_implementation.node_name, node_implementation