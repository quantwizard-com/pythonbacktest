from typing import List
from .dataconsumer import DataConsumer


class DataPropagator(object):

    def __init__(self, consumers: List[DataConsumer] = []):
        self.__consumers = consumers

    def add_consumer(self, data_consumer: DataConsumer):
        if data_consumer in self.__consumers:
            raise ValueError("Duplicate data consumer.")

        self.__consumers.append(data_consumer)

    def distribute_data(self, data_record):
        for consumer in self.__consumers:
            consumer.consume_record(data_record=data_record)