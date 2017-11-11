from typing import Dict

from pythonbacktest.ai.tradeexecutor import AbstractTradeExecutor


class Evaluator(object):
    def __init__(self, evaluation_function_body_compiled):
        self.__evaluation_function_body_compiled = evaluation_function_body_compiled

    def evaluate_new_nodes_values(self, node_results: Dict):
        """
        We have new values for the node. We have to transfer those into transactions.
        :param node_results: Nodes results
        :return: BUY, SELL OR SSELL
        """
        exec_namespace = {'node_results': node_results}

        exec(self.__evaluation_function_body_compiled, exec_namespace)

        buy = exec_namespace['buy']
        sell = exec_namespace['sell']
        ssell = exec_namespace['ssell']

        b = locals()

        if None in [buy, sell, ssell]:
            raise ValueError(f"At least one of the flags is not set. Correct the evaluation function."
                             f"buy: {buy}, sell: {sell}, ssell: {ssell}")

        # at this stage we have 3 variables: buy, sell and ssell
        # calculate recommendations based in that
        if buy + sell + ssell > 1:
            raise ValueError(f"More than one of the flags are set. Correct the evaluation function")

        if buy:
            return "BUY"
        if sell:
            return "SELL"
        if ssell:
            return "SSELL"

        # no recommendation
        return None


