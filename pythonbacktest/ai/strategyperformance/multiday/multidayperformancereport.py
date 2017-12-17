import numpy

class MultidayPerformanceReport(object):

    def __init__(self):
        self.total_gross_pnl = 0
        self.total_net_pnl = 0
        self.total_taxes = 0
        self.total_broker_fees = 0
        self.total_winning_trades = 0
        self.total_losing_trades = 0

        self.total_winning_days = 0
        self.total_losing_days = 0

        self.all_net_pnls = []
        self.all_trade_records = []

        self.performance_record_per_date = None

    def __str__(self):
        return f"Gross PNL:         {self.total_gross_pnl}\n" \
               f"Net PNL:           {self.total_net_pnl}\n" \
               f"Total taxes:       {self.total_taxes}\n" \
               f"Total fees:        {self.total_broker_fees}\n" \
               f"Winning trades:    {self.total_winning_trades}\n" \
               f"Losing trades:     {self.total_losing_trades}\n" \
               f"Min net PnL:       {self.minimum_net_pnl}\n" \
               f"Max net PnL:       {self.maximum_net_pnl}\n" \
               f"STD net PnL:       {self.std_net_pnl}\n" \
               f"Total wining days: {self.total_winning_days}\n" \
               f"Total losing days: {self.total_losing_days}"

    @property
    def minimum_net_pnl(self):
        return min(self.all_net_pnls if self.all_net_pnls else [0])

    @property
    def maximum_net_pnl(self):
        return max(self.all_net_pnls if self.all_net_pnls else [0])

    @property
    def accruing_net_pnl(self):
        result = [0]
        current_accrued_pnl = 0
        for single_pnl in self.all_net_pnls:
            current_accrued_pnl += single_pnl
            result.append(current_accrued_pnl)

        return result

    @property
    def std_net_pnl(self):
        return numpy.std(self.all_net_pnls if self.all_net_pnls else [0])
