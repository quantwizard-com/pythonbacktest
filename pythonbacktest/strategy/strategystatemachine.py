# this class is indended to help building state machine
# for trading strategies

from pythonbacktest.strategy import AbstractTradingStrategy


class StrategyStateMachine(AbstractTradingStrategy):

    def __init__(self):

        # map between state names and handling methods
        self.__states_map = {}

        # current state
        self.__current_state_name = None
        self.__current_price_bar = None
        self.__current_indicators_snapshot = None
        self.__current_latest_indicators_values = None
        self.__is_last_pricebar = False

    def set_states_map(self, states_map):
        if not states_map:
            raise ValueError("states_map")

        self.__states_map = states_map

    def set_current_state(self, state_name):
        if state_name not in self.__states_map:
            raise ValueError("Can't find state definition for state: " + state_name)

        self.__current_state_name = state_name

    def new_price_bar(self, price_bar, indicators_snapshot, latest_indicators_values, broker):
        if self.is_last_pricebar:
            raise AttributeError("self.__is_last_pricebar has already been set. Unexpected price bar")

        self.__pass_price_bar_downstream(price_bar, indicators_snapshot, latest_indicators_values, broker)

    def day_end_price_bar(self, price_bar, indicators_snapshot, latest_indicators_values, broker):

        if self.is_last_pricebar:
            raise AttributeError("self.__is_last_pricebar has already been set. Wrong state of the strategy")

        self.__is_last_pricebar = True
        self.__pass_price_bar_downstream(price_bar, indicators_snapshot, latest_indicators_values, broker)

    def __pass_price_bar_downstream(self, price_bar, indicators_snapshot, latest_indicators_values, broker):
        if self.__states_map is None or not self.__states_map:
            raise ValueError("__states_map is None or empty")

        self.__current_price_bar = price_bar
        self.__current_indicators_snapshot = indicators_snapshot
        self.__current_latest_indicators_values = latest_indicators_values

        state_handling_func = self.__states_map[self.__current_state_name]
        state_handling_func(broker)

    @property
    def current_state_name(self):
        return self.__current_state_name

    @property
    def current_price_bar(self):
        return self.__current_price_bar

    @property
    def current_indicators_snapshot (self):
        return self.__current_indicators_snapshot

    @property
    def current_latest_indicators_values(self):
        return self.__current_latest_indicators_values

    @property
    def is_last_pricebar(self):
        return self.__is_last_pricebar





