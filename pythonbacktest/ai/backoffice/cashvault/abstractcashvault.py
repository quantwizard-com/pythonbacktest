from abc import ABC, abstractmethod


class AbstractCashVault(ABC):

    @abstractmethod
    def available_cash(self):
        raise NotImplementedError()

    @abstractmethod
    def set_available_budget(self, available_budget):
        raise NotImplementedError()

    @abstractmethod
    def modify_available_budget(self, budget_delta):
        raise NotImplementedError()