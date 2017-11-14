from abc import abstractmethod, ABC


class DataConsumer(ABC):

    @abstractmethod
    def consume_record(self, data_record):
        raise NotImplementedError()

