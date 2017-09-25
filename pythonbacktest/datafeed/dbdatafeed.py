import mysql.connector

from .abstractdatafeed import AbstractDataFeed
from .pricebar import PriceBar


class DBDataFeed(AbstractDataFeed):

    def __init__(self, dbhost="localhost", db_user_name="root", db_password="", db_database_name="SecurityPrices"):
        self.__db_host = dbhost
        self.__db_user_name = db_user_name
        self.__db_password = db_password
        self.__db_database_name = db_database_name

        AbstractDataFeed.__init__(self)

    def get_prices_bars_for_day(self, trading_day):
        # this method is not implemented and shouldn't be used for the
        raise Exception("Not implemented method!!!")

    def get_prices_bars_for_day_for_symbol(self, trading_day, security_symbol):
        price_bars = []

        connection = self.__create_connection()

        query = "select pb.Date, pb.Open, pb.Close, pb.High, pb.Low, pb.Volume " \
                "from PriceBars pb, SecurityContracts sc " \
                "where pb.SecurityContractID = sc.ID " \
                "and sc.ContractTickerSymbol = %s " \
                "and Date(pb.Date) = %s " \
                "order by pb.Date asc"

        cursor = connection.cursor()
        cursor.execute(query, (security_symbol, trading_day))

        for (data_date, data_open, data_close, data_high, data_low, data_volume) in cursor:
            price_bar = PriceBar()
            price_bar.timestamp = data_date
            price_bar.open = data_open
            price_bar.close = data_close
            price_bar.high = data_high
            price_bar.low = data_low
            price_bar.volume = data_volume

            price_bars.append(price_bar)

        connection.close()

        return price_bars

    def get_dates_for_symbol_min_data(self, symbol, min_data=1):
        """
        Get dates for symbol where number of data points is at least min_data
        :param symbol: Symbol of the security
        :param min_data: Minimum number of datapoints
        :return: List of dates
        """

        dates = []

        connection = self.__create_connection()

        query = "select date(pb.Date) as single_date " \
                "from PriceBars pb, SecurityContracts sc where pb.SecurityContractID = sc.ID " \
                "and sc.ContractTickerSymbol = %s " \
                "group by single_date " \
                "having count(pb.ID) >= %s " \
                "order by single_date asc"

        cursor = connection.cursor()
        cursor.execute(query, (symbol, min_data))

        for (data_date) in cursor:
            dates.append(data_date)

        connection.close()

        return dates

    def __create_connection(self):
        return mysql.connector.connect(
            host=self.__db_host,
            user=self.__db_user_name,
            password=self.__db_password,
            database=self.__db_database_name)