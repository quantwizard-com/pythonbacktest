from typing import Dict, Text

from .evaluator import Evaluator

class EvaluatorFactory(object):

    ALLOWED_TRANSACTION_NAMES = ['buy', 'sell', 'ssell']

    def create_evaluator(self, evaluator_map: Dict) -> Evaluator:
        """
        Create a new evaluator
        :param evaluator_map: Map of target transaction names (ALLOWED_TRANSACTION_NAMES)
        :return: A new instance of the evaluator
        """
        function_body = self.__create_evaluator_function_body(evaluator_map, "nodes")
        compiled_function_body = self.__compile_function_body(function_body+"\nbeta=567")

        return Evaluator(compiled_function_body)

    def __compile_function_body(self, function_body_def: Text):
        return compile(function_body_def, "<string>", "exec")

    def __create_evaluator_function_body(self, evaluator_map: Dict, nodes_dict_name) -> Text:

        function_body_string_list = []

        for transaction_name, transaction_conditions in evaluator_map.items():
            transaction_name = transaction_name.lower()
            self.__assert_transaction_name(transaction_name)

            current_transaction_string = \
                f"{transaction_name}=" + self.__map_definitions_to_logical_string(transaction_conditions, nodes_dict_name)

            function_body_string_list.append(current_transaction_string)
            
        return "\n".join(function_body_string_list)

    def __map_definitions_to_logical_string(self, transaction_conditions, nodes_dict_name):
        if not transaction_conditions:
            # there're no conditions for the current transaction name - return false
            return "False"

        return " and ".join(
            [self.__single_node_name_to_string(node_name=node_name, nodes_dict_name=nodes_dict_name)
             for node_name in transaction_conditions])

    def __single_node_name_to_string(self, node_name, nodes_dict_name):
        string = "not " if node_name.startswith("!") else ""
        node_name = node_name if not node_name.startswith("!") else node_name[1:]

        return string + f"{nodes_dict_name}['{node_name}'].current_node_result"

    def __assert_transaction_name(self, transaction_name):
        if transaction_name not in self.ALLOWED_TRANSACTION_NAMES:
            raise ValueError(f"Invalid transaction name: {transaction_name}. Allowed: {self.ALLOWED_TRANSACTION_NAMES}")


