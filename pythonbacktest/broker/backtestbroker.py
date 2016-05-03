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

    def go_long(self, number_of_shares):
        self.__check_current_price()

        self.__position += number_of_shares
        self.__budget -= number_of_shares * self.__current_price

    # sell exact number of shares from portfolio
    # if number of shares to sale is more than in portfolio,
    # sell all portfolio to 0, but DON"T go short
    def go_sell(self, number_of_shares):

        if number_of_shares < 0:
            raise "Number of shares to sale should be more than 0"

        number_of_shares_to_sale = number_of_shares if number_of_shares <= self.__position else self.__position

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.__current_price

    # self exact number of shares in portfolio
    # but go short (below 0) if there's not enough shares to sale
    def go_short(self, number_of_shares):
        if number_of_shares < 0:
            raise "Number of shares to sale should be more than 0"

        number_of_shares_to_sale = number_of_shares

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.__current_price

    # get amount of free money on the account
    # that may also include a debt
    def get_free_cash(self):
        return self.__budget

    # get value of all holdings: cash + portfolio (base of the current price)
    def get_current_value(self):
        self.__check_current_price()

        return self.__budget + self.__current_price * self.__position

    # set current price of the security
    def set_current_price(self, current_price):
        self.__current_price = current_price

    # check if current price is set
    def __check_current_price(self):
        if self.current_price is None:
            raise "The current price has not been set!"
