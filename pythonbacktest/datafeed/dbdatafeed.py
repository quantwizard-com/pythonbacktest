import random
import datetime
from collections import OrderedDict

import mysql.connector

from .abstractdatafeed import AbstractDataFeed
from .pricebar import PriceBar


class DBDataFeed(AbstractDataFeed):

    # How many datapoints per day are considered as valid
    # taking into consideration the maximum number of datapoints for stock shares is 4680
    DATA_VALIDITY_NUMBER = 4670

    def __init__(self, dbhost="localhost", db_user_name="root", db_password="", db_database_name="SecurityPrices"):
        self.__db_host = dbhost
        self.__db_user_name = db_user_name
        self.__db_password = db_password
        self.__db_database_name = db_database_name

        AbstractDataFeed.__init__(self)

    def get_prices_bars_for_day_for_symbol(self, trading_day, security_symbol, base_currency_symbol='USD'):
        price_bars = []

        connection = self.__create_connection()

        query = "select pb.Date, pb.Open, pb.Close, pb.High, pb.Low, pb.Volume " \
                "from PriceBars pb, SecurityContracts sc, CurrencySymbols cs  " \
                "where pb.SecurityContractID = sc.ID " \
                "and sc.ContractTickerSymbol = %s " \
                "and Date(pb.Date) = %s " \
                "and sc.ContractCurrencyID = cs.ID " \
                "and cs.CurrencySymbol = %s " \
                "order by pb.Date asc"

        cursor = connection.cursor()
        cursor.execute(query, (security_symbol, trading_day, base_currency_symbol))

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

    def get_all_valid_data_for_symbol(self, ticker, base_currency_symbol='USD'):
        """
        Get all data for the given ticket and base currency assuming that total number of records for the single
        date can't be lower than DATA_VALIDITY_NUMBER (by default: 4670, which is 10 less than maximum number of bars)
        :param ticker: security symbol
        :param base_currency_symbol: base currency (USD by default)
        :return: Ordered dictionary: (key=date, value=list of pricebars per that date)
        """
        result = OrderedDict()

        connection = self.__create_connection()

        query = "select date(pb.Date) as 'date', pb.Date as 'timestamp', pb.Open as 'open', pb.Close as 'close', " \
                "       pb.High as 'high', pb.Low as 'low', pb.Volume as 'volume' " \
                "from PriceBars pb, SecurityContracts sc, CurrencySymbols cs " \
                "where pb.SecurityContractID = sc.ID " \
                "and sc.ContractTickerSymbol = %s " \
                "and Date(pb.Date) in " \
                "(" \
                "   select date(pb1.Date) as single_date " \
                "   from PriceBars pb1, SecurityContracts sc1 " \
                "   where pb1.SecurityContractID = sc1.ID " \
                "   and sc1.ContractTickerSymbol = %s " \
                "   group by single_date " \
                "   having count(pb1.ID) >= %s " \
                ")" \
                "and sc.ContractCurrencyID = cs.ID " \
                "and cs.CurrencySymbol = %s " \
                "order by pb.Date asc;"

        cursor = connection.cursor()
        cursor.execute(query, (ticker, ticker, str(self.DATA_VALIDITY_NUMBER), base_currency_symbol))

        current_date = None
        price_bars_list = []

        for (date, timestamp, data_open, data_close, data_high, data_low, data_volume) in cursor:
            if current_date is None or current_date != date:
                current_date = date
                price_bars_list = []
                result[date] = price_bars_list

            price_bar = PriceBar()
            price_bar.timestamp = timestamp
            price_bar.open = data_open
            price_bar.close = data_close
            price_bar.high = data_high
            price_bar.low = data_low
            price_bar.volume = data_volume

            price_bars_list.append(price_bar)
        connection.close()

        return result

    def get_prices_bars_for_multiple_days_for_symbol(self, security_symbol, *dates) -> OrderedDict:
        result = OrderedDict()

        for single_date in dates:
            if isinstance(single_date, str):
                # convert string to date
                single_date = datetime.datetime.strptime(single_date, "%Y-%m-%d").date()

            result[single_date] = self.get_prices_bars_for_day_for_symbol(single_date, security_symbol)

        return result

    def get_random_sample_of_valid_data_for_symbol(self, security_symbol, number_of_dates_to_extract) -> OrderedDict:
        valid_dates = self.get_valid_dates_for_symbol(security_symbol)
        valid_dates_count = len(valid_dates)

        if valid_dates_count < number_of_dates_to_extract:
            raise ValueError(f"There not enough data to choose from. "
                             f"Valid_dates: {valid_dates_count}, number_of_dates: {number_of_dates_to_extract}")

        random_dates = random.sample(valid_dates, number_of_dates_to_extract)

        result = OrderedDict()

        for date in random_dates:
            result[date] = self.get_prices_bars_for_day_for_symbol(date, security_symbol)

        return result

    def get_valid_dates_for_symbol(self, symbol):
        return self.get_dates_for_symbol_min_data(symbol, min_data=self.DATA_VALIDITY_NUMBER)

    def get_dates_for_symbol_min_data(self, symbol, min_data):
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

        for (data_date,) in cursor:
            dates.append(data_date)

        connection.close()

        return dates

    def __create_connection(self):
        return mysql.connector.connect(
            host=self.__db_host,
            user=self.__db_user_name,
            password=self.__db_password,
            database=self.__db_database_name)