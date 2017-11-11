class TaxCalculator(object):

    @staticmethod
    def calculate_tax(profit):
        """
        Calculate capital gain tax on profit taking into consideration US taxation on foreigners
        :param profit: profit to be taxed
        :return: 0 - there're no capital gain taxes on foreigners
        """
        return 0.0