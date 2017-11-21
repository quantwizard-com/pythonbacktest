class MultidayPerformanceReport(object):

    total_gross_pnl = 0
    total_net_pnl = 0
    total_taxes = 0
    total_broker_fees = 0
    total_winning_trades = 0
    total_losing_trades = 0

    total_winning_days = 0
    total_losing_days = 0

    def __str__(self):
        return f"Gross PNL:         {self.total_gross_pnl}\n" \
               f"Net PNL:           {self.total_net_pnl}\n" \
               f"Total taxes:       {self.total_taxes}\n" \
               f"Total fees:        {self.total_broker_fees}\n" \
               f"Winning trades:    {self.total_winning_trades}\n" \
               f"Losing trades:     {self.total_losing_trades}\n" \
               f"Total wining days: {self.total_winning_days}\n" \
               f"Total losing days: {self.total_losing_days}"
