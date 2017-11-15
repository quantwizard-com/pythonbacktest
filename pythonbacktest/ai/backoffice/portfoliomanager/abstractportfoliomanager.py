from abc import ABC, abstractmethod


class AbstractPortfolioManager(ABC):

    @abstractmethod
    def buy(self, order_size, price_per_share):
        raise NotImplementedError()

    @abstractmethod
    def sell(self, order_size, price_per_share):
        """
        Sell the shares
        :param order_size: Number of shares to sale
        :param price_per_share: Current price per share - required to calculate the profit (loss)
        :return: Profit from the sale
        """
        raise NotImplementedError()

    @abstractmethod
    def portfolio_value(self):
        raise NotImplementedError()

    @abstractmethod
    def current_position_size(self):
        raise NotImplementedError()

    @abstractmethod
    def average_price_per_share(self):
        raise NotImplementedError()
