from .abstractperfcalculator import AbstractPerfCalculator
from pythonbacktest.ai.backoffice.tradehistory import TradeHistory, TradeRecord
from pythonbacktest.ai.strategyperformance import PerformanceReport


class BuySellPerfCalculator(AbstractPerfCalculator):
    SUPPORTED_TRANSACTION_TYPES = ["BUY", "SELL"]

    def __init__(self):
        self.__opening_trade_record: TradeRecord = None

    """
    Strategy performance calculator which applies to buy / sell strategies.
    That is:
    - no short sales
    - 'buy' is considered as a opening transaction
    - 'sell' is considered as a closing transaction
    """

    def calculate_strategy_performance(self, trade_history: TradeHistory) -> PerformanceReport:

        performance_report = PerformanceReport()

        for trade_record in trade_history.trade_records:

            transaction_type = trade_record.transaction_type

            if transaction_type not in self.SUPPORTED_TRANSACTION_TYPES:
                raise ValueError(f"Unsupported transaction type: {transaction_type}")

            if transaction_type == "SELL":
                if not self.__opening_trade_record:
                    raise ValueError("Problem with the trade history. Sell but no Buy")
                performance_report.total_sell_trades += 1

                performance_report.total_taxes += trade_record.tax
                performance_report.total_broker_fees = trade_record.broker_fee
                performance_report.total_gross_pnl = trade_record.gross_transaction_cost - \
                                                     self.__opening_trade_record.gross_transaction_cost
                performance_report.total_net_pnl = trade_record.net_transaction_cost - \
                                                     self.__opening_trade_record.net_transaction_cost

                is_winning_trade = performance_report.total_net_pnl > 0
                performance_report.total_winning_trades += is_winning_trade
                performance_report.total_losing_trades += not is_winning_trade

                self.__opening_trade_record = None
            # endof 'if transaction_type == "SELL"'

            if transaction_type == "BUY":
                if self.__opening_trade_record:
                    raise ValueError("Problem with the trade history. Buy but there's already position open")

                self.__opening_trade_record = trade_record
                performance_report.total_buy_trades += 1
                performance_report.total_broker_fees = trade_record.broker_fee
            # endof 'transaction_type == "BUY"'

        # endof 'for trade_record in trade_history'

        # went through all the transactions - check if there're still positions open
        if self.__opening_trade_record:
            raise ValueError("Went through all the trade records, but there's one buy transaction left open.")

        return performance_report
