from typing import List, Dict

from pythonbacktest.ai.strategyperformance.singleday import SingleDayPerformanceReport
from .multidayperformancereport import MultidayPerformanceReport


class MultidayPerformanceCalculator(object):

    @staticmethod
    def calculate_multiday_performance_report(single_day_performance_reports: Dict):
        performance_report = MultidayPerformanceReport()
        performance_report.performance_record_per_date = single_day_performance_reports

        for single_date, single_day_report in single_day_performance_reports.items():
            performance_report.total_gross_pnl += single_day_report.total_gross_pnl
            performance_report.total_net_pnl += single_day_report.total_net_pnl
            performance_report.all_net_pnls.extend(single_day_report.all_net_pnls)
            performance_report.all_trade_records.extend(single_day_report.all_trade_records)
            performance_report.total_taxes += single_day_report.total_taxes
            performance_report.total_broker_fees += single_day_report.total_broker_fees
            performance_report.total_winning_trades += single_day_report.total_winning_trades
            performance_report.total_losing_trades += single_day_report.total_losing_trades

            performance_report.total_winning_days += single_day_report.total_net_pnl > 0
            performance_report.total_losing_days += single_day_report.total_net_pnl <= 0

        return performance_report
