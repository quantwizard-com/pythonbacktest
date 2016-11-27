# this class is indended to help building state machine
# for trading strategies
import abc

from pythonbacktest.strategy import AbstractTradingStrategy


class StrategyStateMachine(AbstractTradingStrategy):

    def __init__(self):

        # map between state names and handling methods
        self.__states_map = {}

        # name of the current state
        self.__current_state_name = None

        # number of price bars in this state
        # value 1: name of the state
        # value 2: number of pricebars processed in this state
        self.__price_bars_in_state = (None, None)

        self.__current_price_bar = None
        self.__current_indicators_snapshot = None
        self.__current_latest_indicators_values = None
        self.__is_last_pricebar = False
        self.__switch_new_state_name = None
        self.__current_price_bar_index = None

        # current state parameters, to be used by the state; it's reset once the state is switched
        self.__custom_state_params = {}

    @abc.abstractproperty
    def indicator_map(self):
        raise NotImplementedError()

    def set_states_map(self, states_map):
        if not states_map:
            raise ValueError("states_map")

        self.__states_map = states_map

    def set_next_state(self, state_name):
        """
        Set state, which should be called to handler the next price bar
        :param state_name: Next state name
        :return: None
        """
        if state_name not in self.__states_map:
            raise ValueError("Can't find state definition for state: " + state_name)

        if state_name != self.__current_state_name:
            self.__current_state_name = state_name

    def switch_current_state(self, state_name):
        """
        Switch the state from current to the new one.
        State handler will be called AFTER current handler exits.
        Best practice: leave current handler after switching state
        :param state_name: New state after switch
        :return: None
        """
        if state_name not in self.__states_map:
            raise ValueError("Can't find state definition for state: " + state_name)

        self.__switch_new_state_name = state_name

    def track_min_value(self, custom_state_param_name, current_value):
        if custom_state_param_name not in self.__custom_state_params or current_value < self.__custom_state_params[custom_state_param_name]:
            self.__custom_state_params[custom_state_param_name] = current_value

    def track_max_value(self, custom_state_param_name, current_value):
        if custom_state_param_name not in self.__custom_state_params or current_value > self.__custom_state_params[custom_state_param_name]:
            self.__custom_state_params[custom_state_param_name] = current_value

    def new_price_bar(self, price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker):
        if self.is_last_pricebar:
            raise AttributeError("self.__is_last_pricebar has already been set. Unexpected price bar")

        self.__pass_price_bar_downstream(price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker)

    def day_end_price_bar(self, price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker):

        if self.is_last_pricebar:
            raise AttributeError("self.__is_last_pricebar has already been set. Wrong state of the strategy")

        self.__is_last_pricebar = True
        broker.cover_position()

    def __pass_price_bar_downstream(self, price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker):
        if self.__states_map is None or not self.__states_map:
            raise ValueError("__states_map is None or empty")

        self.__current_price_bar = price_bar
        self.__current_indicators_snapshot = indicators_snapshot
        self.__current_latest_indicators_values = latest_indicators_values
        self.__current_price_bar_index = price_bar_index

        self.__call_state_handler(broker=broker)

        # check if the hasn't been switch called
        # in that case: re-call this handler for the new state name
        switch_state_name = self.__switch_new_state_name
        if switch_state_name:
            self.__switch_new_state_name = None
            self.__current_state_name = switch_state_name

            # recall handler for the new state AFTER switching
            self.__pass_price_bar_downstream(price_bar, price_bar_index, indicators_snapshot, latest_indicators_values, broker)

    def __call_state_handler(self, broker):
        state_handling_func = self.__states_map[self.__current_state_name]

        if self.__price_bars_in_state[0] != self.__current_state_name:
            # let's switch current state
            self.__price_bars_in_state = (self.__current_state_name, 1)
            self.__custom_state_params = {}
        else:
            self.__price_bars_in_state = (self.__current_state_name, self.__price_bars_in_state[1] + 1)

        # call the handler
        state_handling_func(broker)

    @property
    def current_state_name(self):
        return self.__current_state_name

    @property
    def price_bars_in_state(self):
        return self.__price_bars_in_state[1]

    @property
    def current_price_bar(self):
        return self.__current_price_bar

    @property
    def current_close(self):
        return self.__current_price_bar.close

    @property
    def current_price_bar_index(self):
        return self.__current_price_bar_index

    @property
    def current_indicators_snapshot(self):
        return self.__current_indicators_snapshot

    @property
    def current_latest_indicators_values(self):
        return self.__current_latest_indicators_values

    @property
    def custom_state_params(self):
        return self.__custom_state_params

    @property
    def is_last_pricebar(self):
        return self.__is_last_pricebar





