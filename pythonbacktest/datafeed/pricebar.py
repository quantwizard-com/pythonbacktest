from typing import Dict


class PriceBar(object):
    timestamp = None
    open = None
    close = None
    high = None
    low = None
    volume = None

    def __init__(self, dict_fields: Dict = None):

        if dict_fields:
            self.timestamp = dict_fields['timestamp']
            self.open = dict_fields['open']
            self.close = dict_fields['close']
            self.high = dict_fields['high']
            self.low = dict_fields['low']
            self.volume = dict_fields['volume']
