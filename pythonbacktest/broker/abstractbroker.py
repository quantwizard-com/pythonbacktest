import abc


class AbstractBroker(object):

    def __init__(self):
        pass

    # buy certain number of shares
    @abc.abstractmethod
    def go_long(self, number_of_shares):
        raise NotImplementedError()

    @abc.abstractmethod
    def go_sell(self, number_of_shares):
        raise NotImplementedError()

    # self exact number of shares in portfolio
    # but go short (below 0) if there's not enough shares to sale
    @abc.abstractmethod
    def go_short(self, number_of_shares):
        raise NotImplementedError()

    # set current position to 0, that is:
    # buy all shorted shares or sell those in portfolio
    @abc.abstractmethod
    def cover_position(self):
        raise NotImplementedError()

    # set current price bar of the security
    @abc.abstractmethod
    def set_current_price_bar(self, current_price_bar, current_price_bar_index):
        raise NotImplementedError()

    # current price of the security
    @abc.abstractproperty
    def current_price(self):
        raise NotImplementedError()

    # get amount of free money on the account
    # that may also include a debt
    @abc.abstractproperty
    def free_cash(self):
        raise NotImplementedError()

    # get value of all holdings: cash + portfolio (base of the current price)
    @abc.abstractproperty
    def current_value(self):
        raise NotImplementedError()

    # number of shares in the portfolio
    @abc.abstractproperty
    def current_position(self):
        raise NotImplementedError()




