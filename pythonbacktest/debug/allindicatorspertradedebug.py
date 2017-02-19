class AllIndicatorsPerTradeDebug(object):
    def render(self, trade_log, *indicators_to_render):

        all_transactions = trade_log.all_transactions

        # check if there're any transaction to render
        if len(all_transactions) == 0:
            print ("Transaction log is empty")
            return

        print (self.__render_header(all_transactions, indicators_to_render))

        for transaction in all_transactions:
            single_transaction_string = ""
            single_transaction_string = self.__append_string_with_tab(single_transaction_string,
                                                                      transaction.price_bar_index_per_day,
                                                                      transaction.timestamp,
                                                                      transaction.transaction_type)

            indicators = transaction.all_indicators_values

            if (indicators_to_render):
                for indicator_name in indicators_to_render:
                    single_transaction_string = self.__append_string_with_tab(single_transaction_string,
                                                                              indicators[indicator_name])
            else:
                for key, value in indicators.iteritems():
                    single_transaction_string = self.__append_string_with_tab(single_transaction_string, value)

            print single_transaction_string

    def __render_header(self, all_transactions, indicators_to_render):
        # set static header fields
        header_string = ""
        header_string = self.__append_string_with_tab(header_string, "Index", "Timestamp", "Type")

        if indicators_to_render:
            for indicator_name in indicators_to_render:
                header_string = self.__append_string_with_tab(header_string, indicator_name)
        else:
            # get first transaction to render the header
            indicators = all_transactions[0].all_indicators_values

            for key, value in indicators.iteritems():
                header_string = self.__append_string_with_tab(header_string, key)

        return header_string

    def __append_string_with_tab(self, target_string, *values_to_append):

        updated_target_string = target_string
        for value_to_append in values_to_append:
            if len(updated_target_string) > 0:
                updated_target_string += "\t"

            updated_target_string += str(value_to_append)

        return updated_target_string
