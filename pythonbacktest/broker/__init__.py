"""
.. moduleauthor:: Krzysztof Wasiak (k.wasiak@gmail.com)
"""
import abc


class AbstractBroker(object):

    @abc.abstractmethod
    def go_long(self, number_of_shares):
        raise NotImplementedError()