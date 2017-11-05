from typing import Dict

from pythonbacktest.ai.tradeexecutor import AbstractTradeExecutor


class Evaluator(object):
    def __init__(self, evaluation_function_body_compiled):
        self.__evaluation_function_body_compiled = evaluation_function_body_compiled

    def new_nodes_values(self, nodes: Dict):
        """
        We have new values for the node. We have to transfer those into transactions.
        :param nodes: Nodes
        :return: BUY, SELL OR SSELL
        """
        buy = None
        sell = None
        ssell = None

        exec(self.__evaluation_function_body_compiled)

        if None in [buy, sell, ssell]:
            raise ValueError(f"At least one of the flags is not set. Correct the evaluation function."
                             f"Buy: {buy}, Sell: {sell}, SSell: {ssell}")

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


