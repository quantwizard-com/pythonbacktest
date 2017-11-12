import unittest
from unittest.mock import MagicMock

from pythonbacktest.ai.transactionevaluator.evaluatorfactory import EvaluatorFactory


class EvaluatorTests(unittest.TestCase):

    def test_one_node_evaluation(self):
        sample_node = True
        node_name = 'sn1'

        evaluator_map = {
            "buy": [node_name],
            "sell": None,
            "ssell": None
        }

        evaluator_factory = EvaluatorFactory()
        evaluator = evaluator_factory.create_evaluator(evaluator_map)

        evaluation_result = evaluator.evaluate_new_nodes_values({node_name: sample_node})

        expected_result = "BUY"

        self.assertEqual(expected_result, evaluation_result)
