class BrokerFeesCalculator(object):

    @staticmethod
    def calculate_broker_fees(order_size, order_value):
        """
        Calculate brokerage fee - considering fees listed for Interactive Brokers
        for US market (https://www.interactivebrokers.com/en/index.php?f=1590&p=stocks1)
        :param order_size: Number of shares
        :param order_value: Total value, how much money flows through order
        :return: Interactive Broker fee for the order
        """
        price_per_share = 0.005
        price_per_order = price_per_share * order_size

        if price_per_order < 1.00:
            return 1.00
        if price_per_order > 0.005 * order_value:
            return 0.005 * order_value

        return price_per_order