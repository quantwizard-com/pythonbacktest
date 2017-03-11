import unittest
from pythonbacktest.indicatorcalculator import IndicatorsCalculatorPerfMonitor


class IndicatorsCalculatorPerfMonitorTests(unittest.TestCase):

    sample_indicator_name_1 = "indicator_1"
    sample_indicator_name_2 = "indicator_2"

    def test_no_data(self):
        perf_monitor = IndicatorsCalculatorPerfMonitor()

        performance_stats = perf_monitor.performance_stats

        self.assertFalse(performance_stats)

    def test_single_indicator(self):
        sample_data = [1, 2, 3, 4]
        perf_monitor = IndicatorsCalculatorPerfMonitor()

        for single_data in sample_data:
            perf_monitor.report_execution_time(self.sample_indicator_name_1, single_data)

        performance_stats = list(perf_monitor.performance_stats)

        # (avg, min, max)
        self.assertEqual((self.sample_indicator_name_1, (2.5, 1, 4)), performance_stats[0])


    def test_two_indicators(self):
        sample_data_1 = [5, 5, 5, 5]
        sample_data_2 = [5, 6, 7, 8]
        perf_monitor = IndicatorsCalculatorPerfMonitor()

        for record_1, record_2 in zip(sample_data_1, sample_data_2):
            perf_monitor.report_execution_time(self.sample_indicator_name_1, record_1)
            perf_monitor.report_execution_time(self.sample_indicator_name_2, record_2)

        performance_stats = list(perf_monitor.performance_stats)

        # (avg, min, max)
        self.assertEqual((self.sample_indicator_name_1, (5, 5, 5)), performance_stats[0])
        self.assertEqual((self.sample_indicator_name_2, (6.5, 5, 8)), performance_stats[1])
