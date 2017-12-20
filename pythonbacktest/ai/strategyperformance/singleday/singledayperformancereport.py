from collections import OrderedDict


class SingleDayPerformanceReport(object):

    def __init__(self):
        # total profit / loss
        self.timestamp = None
        self.total_gross_pnl = 0
        self.total_net_pnl = 0
        self.total_taxes = 0
        self.total_broker_fees = 0
        self.total_winning_trades = 0
        self.total_losing_trades = 0
        self.total_buy_trades = 0
        self.total_sell_trades = 0
        self.total_short_sell_trades = 0

        self.all_net_pnls = []
        self.trade_history = None
        self.indicators_history = None

    def total_trades(self):
        return self.total_buy_trades + self.total_sell_trades + self.total_short_sell_trades

    def __str__(self):
        return f"Gross PNL:         {self.total_gross_pnl}\n" \
               f"Net PNL:           {self.total_net_pnl}\n" \
               f"Total taxes:       {self.total_taxes}\n" \
               f"Total fees:        {self.total_broker_fees}\n" \
               f"Winning trades:    {self.total_winning_trades}\n" \
               f"Losing trades:     {self.total_losing_trades}\n" \
               f"Buy trades:        {self.total_buy_trades}\n" \
               f"Sell trades:       {self.total_sell_trades}\n" \
               f"Short Sell trades: {self.total_short_sell_trades}\n" \
               f"All trades:        {self.all_trades}\n" \
               f"Winning rate:      {self.winning_rate * 100}%"

    @property
    def all_trades(self):
        return self.total_sell_trades \
               + self.total_buy_trades \
               + self.total_short_sell_trades

    @property
    def winning_rate(self):
        return self.total_winning_trades * 1.0 / self.total_sell_trades

    @property
    def minimum_pnl(self):
        return min(self.all_net_pnls)

    @property
    def maximum_pnl(self):
        return max(self.all_net_pnls)

    @property
    def as_dict(self):
        return OrderedDict({
            'Gross PNL': self.total_gross_pnl,
            'Net PNL': self.total_net_pnl,
            'Taxes': self.total_taxes,
            'Broker fees': self.total_broker_fees,
            'Buy trades': self.total_buy_trades,
            'Sell trades': self.total_sell_trades,
            'Short trades': self.total_short_sell_trades,
            'Winning trades': self.total_winning_trades,
            'Losing trades': self.total_losing_trades,
            'Winning rate': f"{self.winning_rate * 100} %",
            'All trades': self.all_trades
        })
