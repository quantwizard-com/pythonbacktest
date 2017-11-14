from pythonbacktest.ai.backoffice.cashvault.abstractcashvault import AbstractCashVault
from pythonbacktest.datafeed import PriceBar
from .abstractbrokergateway import AbstractBrokerGateway

class BacktestBrokerGateway(AbstractBrokerGateway):

    def __init__(self, cash_vault: AbstractCashVault, ):
        super().__init__()

        self.__current_price_bar:PriceBar = None

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
