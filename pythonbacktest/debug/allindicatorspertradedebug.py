class AllIndicatorsPerTradeDebug(object):

    def render(self, trade_log, *indicators_to_render):

        all_transactions = trade_log.all_transactions

        # check if there're any transaction to render
        if len(all_transactions) == 0:
            print ("Transaction log is empty")
            return

        print (self.__render_header(all_transactions, indicators_to_render))

        for transaction in all_transactions:
            single_transaction_string = "%s\t%s\t%s" % (transaction.price_bar_index_per_day, str(transaction.timestamp), transaction.transaction_type)

            indicators = transaction.all_indicators_values

            if (indicators_to_render):
                for indicator_name in indicators_to_render:
                    single_transaction_string += "\t" + str(indicators[indicator_name])
            else:
                for key, value in indicators.iteritems():
                    single_transaction_string += "\t" + str(value)

            print single_transaction_string

    def __render_header(self, all_transactions, indicators_to_render):

        # set static header fields
        header_string = "Index\tTimestamp\tType"

        if indicators_to_render:
            for indicator_name in indicators_to_render:
                header_string += "\t" + indicator_name
        else:
            # get first transaction to render the header
            indicators = all_transactions[0].all_indicators_values

            for key, value in indicators.iteritems():
                header_string += "\t" + key

        return header_string