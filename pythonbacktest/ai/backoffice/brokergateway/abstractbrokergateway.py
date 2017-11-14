from abc import ABC, abstractmethod


class AbstractBrokerGateway(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def buy(self, position_size):
        raise NotImplementedError()

    @abstractmethod
    def sell(self, position_size):
        raise NotImplementedError()

    @abstractmethod
    def short_sell(self, position_size):
        raise NotImplementedError()