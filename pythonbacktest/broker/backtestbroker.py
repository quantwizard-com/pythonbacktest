from . import *


class BackTestBroker(AbstractBroker):

    def __init__(self, budget):
        self.__budget = budget

        # number of shares kept, where
        # >0 - overall portfolio is long
        # <0 - overall portfolio is short
        self.__position = 0

        # what's the current price per share?
        self.__current_price = None

    # set current price of the security
    def set_current_price(self, current_price):
        self.__current_price = current_price

    # buy certain number of shares
    def go_long(self, number_of_shares):
        self.__check_current_price()

        self.__position += number_of_shares
        self.__budget -= number_of_shares * self.__current_price

    # sell exact number of shares from portfolio
    # if number of shares to sale is more than in portfolio,
    # sell all portfolio to 0, but DON"T go short
    def go_sell(self, number_of_shares):

        if number_of_shares < 0:
            raise Exception("Number of shares to sale should be more than 0")

        number_of_shares_to_sale = number_of_shares if number_of_shares <= self.__position else self.__position

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.__current_price

    # self exact number of shares in portfolio
    # but go short (below 0) if there's not enough shares to sale
    def go_short(self, number_of_shares):
        if number_of_shares < 0:
            raise Exception("Number of shares to short should be more than 0")

        number_of_shares_to_sale = number_of_shares

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.__current_price

    def cover_position(self):
        if self.__position < 0:
            self.go_long(-self.__position)
        elif self.__position > 0:
            self.go_sell(self.__position)

    @property
    def current_price(self):
        return self.__current_price

    # get amount of free money on the account
    # that may also include a debt
    @property
    def free_cash(self):
        return self.__budget

    # get value of all holdings: cash + portfolio (base of the current price)
    @property
    def current_value(self):
        self.__check_current_price()

        return self.__budget + self.__current_price * self.__position

    @property
    def current_position(self):
        return self.__position

    # check if current price is set
    def __check_current_price(self):
        if self.current_price is None:
            raise Exception("The current price has not been set!")
