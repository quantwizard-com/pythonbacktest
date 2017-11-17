class TradeDataSnapshot(object):
    """
    This is snapshot of the current status of the backoffice across multiple elements,
    like: cash vault, trade history, portfolio manager, etc.
    """

    def __init__(self, current_position_size, current_budget):
        self.__current_position_size = current_position_size
        self.__current_budget = current_budget

    @property
    def current_position_size(self):
        return self.__current_position_size

    @property
    def current_budget(self):
        return self.__current_budget
