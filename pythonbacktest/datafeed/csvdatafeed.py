import os
import csv

from os import path
from datetime import datetime
from . import abstractdatafeed as adf, pricebar as pb, tradingdaydata as tdd


class CSVDataFeed(adf.AbstractDataFeed):
    def __init__(self):
        # data feed data storage - dictionary
        # key - date of the data
        # value - collection of TradingDayData ordered by date for the given day
        self.__data = {}
        self.__data_view_range = (0, None)

        adf.AbstractDataFeed.__init__(self)

    def get_prices_bars_for_day(self, trading_day):
        if self.__data_view_range[1] is None:
            return self.__data[trading_day].price_bars[self.__data_view_range[0]:]
        else:
            return self.__data[trading_day].price_bars[self.__data_view_range[0]:self.__data_view_range[1] + 1]

    def load_data(self, source_location):

        if path.isdir(source_location):
            self.load_data_from_directory(source_location)

        elif path.isfile(source_location):
            self.load_data_from_file(source_location)

        else:
            raise Exception("Source location doesn't exist")

    def load_data_from_directory(self, source_directory):

        for file_name in os.listdir(source_directory):
            if file_name.endswith(".csv"):
                self.load_data_from_file(source_directory + "/" + file_name)

        return None

    def load_data_from_file(self, source_file):

        price_bars = []
        current_date = None

        with open(source_file, 'rt') as source_file:
            data_reader = csv.reader(source_file, delimiter=',')

            first_row = True

            for row in data_reader:

                if not first_row:
                    single_bar = pb.PriceBar()
                    single_bar.timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    single_bar.open = float(row[1])
                    single_bar.close = float(row[2])
                    single_bar.high = float(row[3])
                    single_bar.low = float(row[4])
                    single_bar.volume = float(row[5])

                    price_bars.append(single_bar)

                    if current_date is None:
                        current_date = single_bar.timestamp.date()

                first_row = False

        # now: add downloaded bars to the storage
        if current_date not in self.__data:
            self.__data[current_date] = tdd.TradingDayData(price_bars, current_date)
        else:
            raise "There's already data for given date: " + current_date
