import unittest

from pythonbacktest.ai.transactionevaluator.evaluatorfactory import EvaluatorFactory


class EvaluatorFactoryTests(unittest.TestCase):

    def test_create_evaluator_single_node_name(self):

        evaluator_map = {
            "buy": ["sn_buy_1"],
            "sell": None,
            "ssell": None
        }
        nodes_dict_name = "nodes1234"

        evaluator_factory = EvaluatorFactory()

        function_body = evaluator_factory._EvaluatorFactory__create_evaluator_function_body(evaluator_map, nodes_dict_name)

        expected_body = f"buy={nodes_dict_name}['sn_buy_1']\nsell=False\nssell=False"

        self.assertEqual(expected_body, function_body)

    def test_create_evaluator_single_negative_node_name(self):

        evaluator_map = {
            "buy": ["!sn_buy_1"],
            "sell": None,
            "ssell": None
        }
        nodes_dict_name = "nodes1234"

        evaluator_factory = EvaluatorFactory()
        function_body = evaluator_factory._EvaluatorFactory__create_evaluator_function_body(evaluator_map, nodes_dict_name)
        expected_body = f"buy=not {nodes_dict_name}['sn_buy_1']\nsell=False\nssell=False"

        self.assertEqual(expected_body, function_body)


    def test_create_evaluator_negative_sell_node(self):

        evaluator_map = {
            "buy": ["sn_buy_1", "sn_buy_2"],
            "sell": ["sn_sell_1", "!sn_sell_2"],
            "ssell": None
        }
        nodes_dict_name = "nodes1234"

        evaluator_factory = EvaluatorFactory()

        function_body = evaluator_factory._EvaluatorFactory__create_evaluator_function_body(evaluator_map, nodes_dict_name)

        expected_body = f"buy={nodes_dict_name}['sn_buy_1'] and " \
                        f"{nodes_dict_name}['sn_buy_2']\n" \
                        f"sell={nodes_dict_name}['sn_sell_1'] and " \
                        f"not {nodes_dict_name}['sn_sell_2']\nssell=False"

        self.assertEqual(expected_body, function_body)
