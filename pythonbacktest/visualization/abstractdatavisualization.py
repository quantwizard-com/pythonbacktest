from abc import ABC, abstractmethod


class AbstractDataVisualization(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def render_charts(self, indicators_history, indicators_to_display):
        raise NotImplemented
