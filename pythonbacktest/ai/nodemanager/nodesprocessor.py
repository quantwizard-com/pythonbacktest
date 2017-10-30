from ai.nodemanager.nodesmap import NodesMap
from pythonbacktest.ai.utils.indicatorshistorysource import IndicatorsHistorySource


class NodesProcessor(object):

    def __init__(self, source_nodes_map: NodesMap):
        self.__source_nodes_map = source_nodes_map

    def process_all_nodes_on_indicators_history(self):
        while True:
            if not self.__source_nodes_map.move_to_next_indicators_snapshot_record():
                break

