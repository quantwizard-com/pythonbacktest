from . import *


class BackTestBroker(AbstractBroker):

    def __init__(self, budget, trade_log=None, commision=0.0):
        AbstractBroker.__init__(self)

        self.__budget = budget
        self.__commision = commision

        # number of shares kept, where
        # >0 - overall portfolio is long
        # <0 - overall portfolio is short
        self.__position = 0

        self.__avg_price_per_share = 0

        # what's the current price per share?
        self.__current_price_bar = None
        self.__current_price_bar_index = None

        self.__trade_log = trade_log

        self.__indicators = None

    # set current price of the security
    def set_current_price_bar(self, current_price_bar, current_price_bar_index):
        self.__current_price_bar = current_price_bar
        self.__current_price_bar_index = current_price_bar_index

    # set Indicators object, which will be used to collect trade markets
    def set_indicators(self, indicators):
        self.__indicators = indicators

    # buy certain number of shares
    def go_long(self, number_of_shares, comment=None):
        self.__check_current_price()

        # update average price per share
        self.__avg_price_per_share = \
            (self.__avg_price_per_share * self.__position + number_of_shares * self.current_price) / (self.__position + number_of_shares)

        self.__position += number_of_shares
        self.__budget -= number_of_shares * self.current_price
        self.__charge_commission()

        self.__log_trade("BUY", number_of_shares, comment=comment)

    # sell exact number of shares from portfolio
    # if number of shares to sale is more than in portfolio,
    # sell all portfolio to 0, but DON"T go short
    def go_sell(self, number_of_shares, comment=None):

        if number_of_shares < 0:
            raise Exception("Number of shares to sale should be more than 0")

        number_of_shares_to_sale = number_of_shares if number_of_shares <= self.__position else self.__position

        # update average price per share
        if self.__position == number_of_shares_to_sale:
            self.__avg_price_per_share = 0
        else:
            self.__avg_price_per_share = \
                (self.__avg_price_per_share * self.__position - number_of_shares_to_sale * self.current_price) / (self.__position - number_of_shares_to_sale)

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.current_price
        self.__charge_commission()

        self.__log_trade("SELL", number_of_shares, comment=comment)

    # self exact number of shares in portfolio
    # but go short (below 0) if there's not enough shares to sale
    def go_short(self, number_of_shares, comment=None):
        if number_of_shares < 0:
            raise Exception("Number of shares to short should be more than 0")

        number_of_shares_to_sale = number_of_shares

        self.__position -= number_of_shares_to_sale
        self.__budget += number_of_shares_to_sale * self.current_price
        self.__charge_commission()

        self.__log_trade("SHORT", number_of_shares, comment=comment)

    def cover_position(self, comment=None):
        if self.__position < 0:
            self.go_long(-self.__position, comment=comment)
        elif self.__position > 0:
            self.go_sell(self.__position, comment=comment)

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

    @property
    def avg_price_per_share(self):
        return self.__avg_price_per_share

    # check if current price is set
    def __check_current_price(self):
        if self.current_price is None:
            raise Exception("The current price has not been set!")

    # deduct the trade commission
    def __charge_commission(self):
        self.__budget -= self.__commision

    def __log_trade(self, transaction_type, shares_amount, comment=None):
        if self.__indicators is not None:
            self.__indicators.mark_transaction(transaction_type, self.current_price)

        if self.__trade_log is not None:
            self.__trade_log.log_transaction(
                price_bar_index_per_day=self.__current_price_bar_index,
                price_bar_time_stamp=self.__current_price_bar.timestamp,
                transaction_type=transaction_type,
                shares_amount=shares_amount,
                transaction_price_per_share=self.current_price,
                cash_spent=shares_amount * self.current_price,
                cash_after=self.free_cash,
                position_after=self.current_position,
                comment=comment)
