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
        current_price_per_share = self.__get_current_price_per_share()
        stock_only_price = current_price_per_share * position_size
        transaction_price = current_price_per_share

        broker_fees = 0
        if self.__apply_broker_fees:
            broker_fees = self.__fees_calculator.calculate_broker_fees(position_size, stock_only_price)
        transaction_price += broker_fees

        self.__portfolio_manager.buy(position_size, current_price_per_share)
        self.__cash_vault.modify_available_budget(-transaction_price)

        # record the transaction
        self.__trade_history.new_transaction(self.__current_price_bar, "BUY", position_size,
                                             current_price_per_share, self.__cash_vault.available_cash,
                                             broker_fees, tax=0)

    def sell(self, position_size):
        current_price_per_share = self.__get_current_price_per_share()
        stock_only_price = current_price_per_share * position_size
        transaction_gain = current_price_per_share

        broker_fees = 0
        if self.__apply_broker_fees:
            broker_fees = self.__fees_calculator.calculate_broker_fees(position_size, stock_only_price)
        transaction_gain -= broker_fees

        sell_profit = self.__portfolio_manager.sell(position_size, current_price_per_share)

        tax = 0
        if self.__apply_tax and sell_profit > 0:
            tax = self.__tax_calculator.calculate_tax(sell_profit)
        transaction_gain -= tax

        self.__cash_vault.modify_available_budget(transaction_gain)

        # record the transaction
        self.__trade_history.new_transaction(self.__current_price_bar, "SELL", position_size,
                                             current_price_per_share, self.__cash_vault.available_cash,
                                             broker_fee=broker_fees, tax=tax)

    def short_sell(self, position_size):
        raise NotImplementedError()

    def set_current_price_bar(self, price_bar: PriceBar):
        if self.__current_price_bar:
            if price_bar.timestamp == self.__current_price_bar.timestamp:
                raise ValueError("New price bar is the same as the old one...")

        self.__current_price_bar = price_bar

    def __get_current_price_per_share(self):
        return self.__current_price_bar.close

    @property
    def trade_history(self):
        return self.__trade_history

    @property
    def cash_vault(self):
        return self.__cash_vault

    @property
    def portfolio_manager(self):
        return self.__portfolio_manager
