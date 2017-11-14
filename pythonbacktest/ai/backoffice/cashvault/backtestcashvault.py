from .abstractcashvault import AbstractCashVault


class BacktestCashVault(AbstractCashVault):

    def __init__(self, initial_budget):
        super().__init__()

        self.__current_budget = initial_budget

    @property
    def available_cash(self):
        return self.__current_budget

    def set_available_budget(self, available_budget):
        self.__current_budget = available_budget

    def modify_available_budget(self, budget_delta):
        self.__current_budget += budget_delta
        return self.__current_budget
