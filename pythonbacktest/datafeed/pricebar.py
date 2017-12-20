from typing import Dict

from collections import OrderedDict


class PriceBar(object):
    def __init__(self, dict_fields: Dict = None):

        if dict_fields:
            self.timestamp = dict_fields['timestamp']
            self.open = dict_fields['open']
            self.close = dict_fields['close']
            self.high = dict_fields['high']
            self.low = dict_fields['low']
            self.volume = dict_fields['volume']

    def __str__(self):
        return f"timestamp: {self.timestamp}; open: {self.open}; close: {self.close}; " \
               f"high: {self.high}; low: {self.low}; volume: {self.volume}"

    @property
    def as_dict(self):
        return OrderedDict({
            'timestamp': self.timestamp,
            'open': self.open,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'volume': self.volume
        })
