class PerformanceReport(object):

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

    def total_trades(self):
        return self.total_buy_trades + self.total_sell_trades + self.total_short_sell_trades
