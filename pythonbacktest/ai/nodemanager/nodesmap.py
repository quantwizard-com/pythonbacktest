from typing import List

from pythonbacktest.indicatorshistory import IndicatorHistory
from pythonbacktest.ai.utils.indicatorshistorysource import IndicatorsHistorySource
from pythonbacktest.ai.nodes.base import AbstractNode


class NodesMap(object):

    def __init__(self, nodes_map_definition, indicators_history: IndicatorHistory):
        self.__all_nodes: List[AbstractNode] = []
        self.__name_to_node_map = {}
        self.__indicators_history_source = IndicatorsHistorySource(indicators_history)

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

            # make sure the indicators history source is set
            node_implementation.set_indicators_history_source(self.__indicators_history_source)

            self.__name_to_node_map[node_name] = node_implementation
            self.__all_nodes.append(node_implementation)

    def move_to_next_indicators_snapshot_record(self) -> bool:
        for single_node in self.__all_nodes:
            # indicators_source is already passed to each node, so doesn't have to pushed again
            single_node.activate_node()

        return self.__indicators_history_source.move_to_next_timestamp()

    def __unpack_node_map_definition(self, record) -> tuple:
        node_source_specs = record['sourcenodes']
        node_implementation: AbstractNode = record['nodeimplementation']

        if not node_implementation:
            raise ValueError('Node implementation is not defined')

        return node_implementation.node_name, node_implementation