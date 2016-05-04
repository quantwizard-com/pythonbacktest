class TradingDayData:

    def __init__(self, pricebars, tradingday):
        self.__pricebars = pricebars
        self.__tradingday = tradingday

    @property
    def price_bars(self):
        return self.__pricebars
