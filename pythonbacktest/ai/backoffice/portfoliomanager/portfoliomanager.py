from .abstractportfoliomanager import AbstractPortfolioManager


class PortfolioManager(AbstractPortfolioManager):

    def __init__(self):
        self.__current_position_size = 0
        self.__average_price_per_share = 0

    def buy(self, order_size, price_per_share):
        old_position_size = self.__current_position_size
        old_price_per_share = self.__average_price_per_share
        old_portfolio_value = old_position_size * old_price_per_share

        order_value = order_size * price_per_share
        new_portfolio_value = order_value + old_portfolio_value
        new_portfolio_size = old_position_size + order_size

        self.__average_price_per_share = new_portfolio_value * 1.0 / new_portfolio_size
        self.__current_position_size = new_portfolio_size

    def sell(self, order_size):
        available_to_sale = self.__current_position_size
        if order_size > available_to_sale:
            raise ValueError(f"You want to sell {order_size} shares, but only {available_to_sale} are available")

        if order_size == available_to_sale:
            self.__average_price_per_share = 0

        self.__current_position_size -= order_size

    @property
    def portfolio_value(self):
        return self.__current_position_size * self.__average_price_per_share

    @property
    def current_position_size(self):
        return self.__current_position_size

    @property
    def average_price_per_share(self):
        return self.__average_price_per_share
