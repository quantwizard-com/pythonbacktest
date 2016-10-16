import unittest

from mock import MagicMock

from pythonbacktest.broker import BackTestBroker
from pythonbacktest.datafeed import PriceBar
from pythonbacktest.strategy import StrategyStateMachine


class StrategyStateMachineTests(unittest.TestCase):

    def test_properties_set_on_new_pricebar(self):
        state_machine = StrategyStateMachine()

        state_handler_1 = MagicMock()
        state_handler_2 = MagicMock()
        state_handler_3 = MagicMock()

        state_map = {"state1": state_handler_1, "state2": state_handler_2, "state3": state_handler_3}

        state_machine.set_states_map(states_map=state_map)

        price_bar = PriceBar()
        indicators_snapshot = "Indicators snapshot"
        latest_indicators_values = "Latest Indicators values"
        broker = "broker"

        state_machine.set_next_state("state1")
        state_machine.new_price_bar(price_bar=price_bar,
                                    price_bar_index=5,
                                    indicators_snapshot=indicators_snapshot,
                                    latest_indicators_values=latest_indicators_values,
                                    broker=broker)

        args, kwargs = state_handler_1.call_args

        self.assertEqual(broker, args[0])

        self.assertEqual(indicators_snapshot, state_machine.current_indicators_snapshot)
        self.assertEqual(latest_indicators_values, state_machine.current_latest_indicators_values)
        self.assertEqual(price_bar, state_machine.current_price_bar)
        self.assertEqual("state1", state_machine.current_state_name)
        self.assertFalse(state_machine.is_last_pricebar)

    def test_properties_set_on_lastpricebar(self):
        state_machine = StrategyStateMachine()

        state_handler_1 = MagicMock()
        state_handler_2 = MagicMock()
        state_handler_3 = MagicMock()

        state_map = {"state1": state_handler_1, "state2": state_handler_2, "state3": state_handler_3}

        state_machine.set_states_map(states_map=state_map)

        price_bar = PriceBar()
        indicators_snapshot = "Indicators snapshot"
        latest_indicators_values = "Latest Indicators values"

        broker = MagicMock()
        cover_position_mock = MagicMock()
        broker.cover_position = cover_position_mock

        state_machine.set_next_state("state3")
        state_machine.day_end_price_bar(price_bar=price_bar,
                                        price_bar_index=5,
                                        indicators_snapshot=indicators_snapshot,
                                        latest_indicators_values=latest_indicators_values,
                                        broker=broker)

        self.assertTrue(state_machine.is_last_pricebar)
        cover_position_mock.assert_called()

    def test_properties_set_on_new_pricebar_and_state_switch(self):
        state_machine = StrategyStateMachine()

        state_handler_1 = lambda broker: state_machine.switch_current_state("state2")
        state_handler_2 = lambda broker: state_machine.switch_current_state("state3")
        state_handler_3 = MagicMock()

        state_map = {"state1": state_handler_1, "state2": state_handler_2, "state3": state_handler_3}

        state_machine.set_states_map(states_map=state_map)

        price_bar = PriceBar()
        indicators_snapshot = "Indicators snapshot"
        latest_indicators_values = "Latest Indicators values"
        broker = "broker"

        state_machine.set_next_state("state1")
        state_machine.new_price_bar(price_bar=price_bar,
                                    price_bar_index=5,
                                    indicators_snapshot=indicators_snapshot,
                                    latest_indicators_values=latest_indicators_values,
                                    broker=broker)

        args, kwargs = state_handler_3.call_args

        self.assertEqual(broker, args[0])

        self.assertEqual(indicators_snapshot, state_machine.current_indicators_snapshot)
        self.assertEqual(latest_indicators_values, state_machine.current_latest_indicators_values)
        self.assertEqual(price_bar, state_machine.current_price_bar)
        self.assertEqual("state3", state_machine.current_state_name)
        self.assertFalse(state_machine.is_last_pricebar)
        self.assertEqual(1, state_machine.price_bars_in_state)

        # let's call the handler again

        state_machine.new_price_bar(price_bar=price_bar,
                                    price_bar_index=5,
                                    indicators_snapshot=indicators_snapshot,
                                    latest_indicators_values=latest_indicators_values,
                                    broker=broker)

        args, kwargs = state_handler_3.call_args

        self.assertEqual(broker, args[0])

        self.assertEqual(indicators_snapshot, state_machine.current_indicators_snapshot)
        self.assertEqual(latest_indicators_values, state_machine.current_latest_indicators_values)
        self.assertEqual(price_bar, state_machine.current_price_bar)
        self.assertEqual("state3", state_machine.current_state_name)
        self.assertFalse(state_machine.is_last_pricebar)
        self.assertEqual(2, state_machine.price_bars_in_state)



