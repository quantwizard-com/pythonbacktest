from . import *


class BackTestBroker(AbstractBroker):

    def __init__(self, budget, trade_log=None):
        AbstractBroker.__init__(self)

        self.__budget = budget

        # number of shares kept, where
        # >0 - overall portfolio is long
        # <0 - overall portfolio is short
        self.__position = 0

        # what's the current price per share?
        self.__current_price_bar = None

        self.__trade_log = trade_log

    # set current price of the security
    def set_current_price_bar(self, current_price_bar):
        self.__current_price_bar = current_price_bar

    # buy certain number of shares
    def go_long(self, number_of_shares):
        self.__check_current_price()

        self.__position += number_of_shares
        self.__budget -= number_of_shares * self.current_price

        self.__log_trade("BUY", number_of_shares)

    # sell exact number of shares from portfolio
    # if number of shares to sale is more than in portfolio,
    # sell all portfolio to 0, but DON"T go short
    def go_sell(self, number_of_shares):

        if number_of_shares < 0:
            raise Exception("Number of shares to sale should be more than 0")

        number_of_shares_to_sale = number_of_shares if number_of_shares <= self.__position else self.__position

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.current_price

        self.__log_trade("SELL", number_of_shares)

    # self exact number of shares in portfolio
    # but go short (below 0) if there's not enough shares to sale
    def go_short(self, number_of_shares):
        if number_of_shares < 0:
            raise Exception("Number of shares to short should be more than 0")

        number_of_shares_to_sale = number_of_shares

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.current_price

        self.__log_trade("SHORT", number_of_shares)

    def cover_position(self):
        if self.__position < 0:
            self.go_long(-self.__position)
        elif self.__position > 0:
            self.go_sell(self.__position)

    @property
    def current_price(self):
        return self.__current_price_bar.close

    # get amount of free money on the account
    # that may also include a debt
    @property
    def free_cash(self):
        return self.__budget

    # get value of all holdings: cash + portfolio (base of the current price)
    @property
    def current_value(self):
        self.__check_current_price()

        return self.__budget + self.current_price * self.__position

    @property
    def current_position(self):
        return self.__position

    # check if current price is set
    def __check_current_price(self):
        if self.current_price is None:
            raise Exception("The current price has not been set!")

    def __log_trade(self, transaction_type, shares_amount):
        if self.__trade_log is not None:
            self.__trade_log.log_transaction(None, transaction_type, shares_amount,
                                        self.current_price, shares_amount * self.current_price,
                                        self.free_cash, self.current_position)
