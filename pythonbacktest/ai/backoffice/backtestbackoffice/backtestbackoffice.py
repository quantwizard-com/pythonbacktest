from typing import Text

from pythonbacktest.ai.backoffice.brokergateway.backtestbrokergateway import BacktestBrokerGateway
from pythonbacktest.ai.backoffice.cashvault.abstractcashvault import AbstractCashVault
from pythonbacktest.ai.backoffice.portfoliomanager.abstractportfoliomanager import AbstractPortfolioManager
from pythonbacktest.datafeed import PriceBar


class BackTestBackOffice(object):

    def __init__(self, broker_gateway: BacktestBrokerGateway,
                    cash_vault: AbstractCashVault,
                    portfolio_manager: AbstractPortfolioManager,
                    default_transaciton_size):

        self.TRANSACTION_NAME_TO_FUNCTION = {
            "buy": self.buy,
            "sell": self.sell,
            "ssell": self.short_sell
        }

        self.__broker_gateway = broker_gateway
        self.__cash_vault = cash_vault
        self.__portfolio_manager = portfolio_manager
        self.__default_transaction_size = default_transaciton_size

    def execute_transaction(self, transaction_name: Text):
        if not transaction_name:
            raise ValueError("Empty transaction_name passed to the function")

        transaction_name = transaction_name.lower()
        if transaction_name not in self.TRANSACTION_NAME_TO_FUNCTION:
            raise ValueError(f"Unknown transaction name: {transaction_name}")

        self.TRANSACTION_NAME_TO_FUNCTION[transaction_name]()

    def buy(self):
        self.__broker_gateway.buy(self.__default_transaction_size)

    def sell(self):
        self.__broker_gateway.sell(self.__default_transaction_size)

    def short_sell(self):
        self.__broker_gateway.short_sell(self.__default_transaction_size)

    def set_price_bar(self, price_bar: PriceBar):
        self.__broker_gateway.set_current_price_bar(price_bar)

