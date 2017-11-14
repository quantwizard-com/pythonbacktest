from pythonbacktest.ai.backoffice.brokergateway.abstractbrokergateway import AbstractBrokerGateway
from pythonbacktest.ai.tradehistory.tradehistory import TradeHistory
from pythonbacktest.datafeed import PriceBar
from .abstracttradeexecutor import AbstractTradeExecutor


class BackTestTradeExecutor(AbstractTradeExecutor):

    def __init__(self, trade_history: TradeHistory, broker_gateway: AbstractBrokerGateway):
        super().__init__(trade_history)
        self.__current_price_bar = None
        self.__broker_gateway = broker_gateway

    def set_current_price_bar(self, price_bar: PriceBar):
        if not price_bar:
            raise ValueError("price_bar can't be None")

        if price_bar == self.__current_price_bar:
            raise ValueError("The new price_bar is identical as the previous one..."
                             "")
        self.__current_price_bar = price_bar

    def sell(self, position_size):
        self.trade_history.new_transaction()

    def buy(self, position_size):
        pass

    def short_sell(self, position_size):
        pass

    @property
    def broker_gateway(self):
        return self.__broker_gateway

    def __assert_input_values(self):
        if not self.__current_price_bar:
            raise ValueError('Current pricebar is not set')

