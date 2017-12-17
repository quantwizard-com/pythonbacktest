from abc import ABC, abstractmethod

from pythonbacktest.indicatorshistory import IndicatorHistory
from pythonbacktest.ai.backoffice.tradehistory import TradeHistory
from pythonbacktest.ai.strategyperformance.singleday import SingleDayPerformanceReport


class AbstractPerfCalculator(ABC):

    @abstractmethod
    def calculate_strategy_performance(self,
                                       indicators_history: IndicatorHistory,
                                       trade_history: TradeHistory) -> SingleDayPerformanceReport:
        raise NotImplementedError()
