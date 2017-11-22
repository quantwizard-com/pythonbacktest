class SingleDayPerformanceReport(object):

    # total profit / loss
    total_gross_pnl = 0
    total_net_pnl = 0
    total_taxes = 0
    total_broker_fees = 0
    total_winning_trades = 0
    total_losing_trades = 0
    total_buy_trades = 0
    total_sell_trades = 0
    total_short_sell_trades = 0

    all_net_pnls = []

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
