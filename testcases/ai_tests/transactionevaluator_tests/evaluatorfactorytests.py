import unittest

from pythonbacktest.ai.transactionevaluator.evaluatorfactory import EvaluatorFactory


class EvaluatorFactoryTests(unittest.TestCase):

    def test_create_evaluator_function_body_single_node_name(self):

        evaluator_map = {
            "buy": ["sn_buy_1"],
            "sell": None,
            "ssell": None
        }
        nodes_dict_name = "nodes1234"

        evaluator_factory = EvaluatorFactory()

        function_body = evaluator_factory._EvaluatorFactory__create_evaluator_function_body(evaluator_map, nodes_dict_name)

        expected_body = f"buy={nodes_dict_name}['sn_buy_1'].current_node_result\nsell=False\nssell=False"

        self.assertEqual(expected_body, function_body)

