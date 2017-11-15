from pythonbacktest.ai.backoffice.backtestbackoffice.backtestbackoffice import BackTestBackOffice
from pythonbacktest.ai.tradehistory.tradehistory import TradeHistory
from pythonbacktest.ai.backoffice.brokergateway.backtestbrokergateway import BacktestBrokerGateway
from pythonbacktest.ai.backoffice.cashvault.backtestcashvault import BacktestCashVault
from pythonbacktest.ai.backoffice.feescalculators.brokerfeescalculator import BrokerFeesCalculator
from pythonbacktest.ai.backoffice.feescalculators.taxcalculator import TaxCalculator
from pythonbacktest.ai.backoffice.portfoliomanager.portfoliomanager import PortfolioManager


class BackOfficeFactory(object):

    @staticmethod
    def create_back_test_back_office(initial_budget,
                                     default_transaction_size,
                                     apply_tax=True,
                                     apply_broker_fees=True) -> BackTestBackOffice:
        cash_vault = BacktestCashVault(initial_budget=initial_budget)
        portfolio_manager = PortfolioManager()
        tax_calculator = TaxCalculator()
        fees_calculator = BrokerFeesCalculator()
        trade_history = TradeHistory()

        broker_gateway = BacktestBrokerGateway(
            cash_vault=cash_vault, portfolio_manager=portfolio_manager,
            tax_calculator=tax_calculator, fees_calculator=fees_calculator,
            trade_history=trade_history,
            apply_tax=apply_tax, apply_broker_fees=apply_broker_fees
        )

        return BackTestBackOffice(broker_gateway,
                                  cash_vault,
                                  portfolio_manager,
                                  default_transaciton_size=default_transaction_size)
