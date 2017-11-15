from pythonbacktest.ai.tradehistory.tradehistory import TradeHistory
from pythonbacktest.ai.backoffice.feescalculators.brokerfeescalculator import BrokerFeesCalculator
from pythonbacktest.ai.backoffice.feescalculators.taxcalculator import TaxCalculator
from pythonbacktest.ai.backoffice.portfoliomanager.abstractportfoliomanager import AbstractPortfolioManager
from pythonbacktest.ai.backoffice.cashvault.abstractcashvault import AbstractCashVault
from pythonbacktest.datafeed import PriceBar
from .abstractbrokergateway import AbstractBrokerGateway


class BacktestBrokerGateway(AbstractBrokerGateway):

    def __init__(self, cash_vault: AbstractCashVault,
                 portfolio_manager: AbstractPortfolioManager,
                 tax_calculator: TaxCalculator,
                 fees_calculator: BrokerFeesCalculator,
                 trade_history: TradeHistory,
                 apply_tax, apply_broker_fees):
        super().__init__()

        self.__current_price_bar: PriceBar = None
        self.__cash_vault = cash_vault
        self.__portfolio_manager = portfolio_manager
        self.__tax_calculator = tax_calculator
        self.__fees_calculator = fees_calculator
        self.__trade_history = trade_history
        self.__apply_tax = apply_tax
        self.__apply_broker_fees = apply_broker_fees

    def buy(self, position_size):
        pass

    def sell(self, position_size):
        pass

    def short_sell(self, position_size):
        pass

    def set_current_price_bar(self, price_bar: PriceBar):
        if self.__current_price_bar:
            if price_bar.timestamp == self.__current_price_bar.timestamp:
                raise ValueError("New price bar is the same as the old one...")

        self.__current_price_bar = price_bar
